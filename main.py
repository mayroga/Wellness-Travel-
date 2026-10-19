
import os
import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
MAX_TEXT = 10000
TIMEOUT = httpx.Timeout(30.0, connect=10.0)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mayroga.liveenglish")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=TIMEOUT)
    yield
    await app.state.client.aclose()


app = FastAPI(
    title="MAY ROGA Live English",
    version="1.2.0",
    lifespan=lifespan
)


class ConversationRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)
    context: str = Field(default="", max_length=5000)
    mode: str = Field(
        default="conversation",
        pattern="^(conversation|interview)$"
    )


class TranslationRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)


def parse_json_response(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except (ValueError, TypeError):
        pass

    return {"answer": text[:2500], "note": ""}


def response_prompt(transcript: str, context: str, mode: str) -> str:
    if mode == "interview":
        mode_instructions = """
MODE: QUESTIONS AND ANSWERS / INTERVIEW

The user may be speaking with a recruiter, interviewer, manager,
coworker, or professional contact.

- If the latest speech is an interview question, write a concise,
  professional answer the user can say aloud in English.
- Prefer simple, natural English that is easy to understand and repeat.
- Use the conversation context to understand the question.
- Never invent the user's education, licenses, skills, experience,
  achievements, availability, salary expectations, or personal facts.
- If the answer depends on information you do not know, suggest an
  honest response or a polite question asking for clarification.
- If the latest speech is not an interview question, respond naturally
  to what the other person said.
"""
    else:
        mode_instructions = """
MODE: LIVE CONVERSATION

Help the user participate in a real-time English conversation.

- Suggest the actual words the user can say next in English.
- Respond naturally to the other person's latest statement or question.
- For greetings, give a suitable greeting in return.
- For questions, answer directly when enough information is available.
- For instructions, suggest an appropriate acknowledgement or follow-up.
- If the other person asks for personal information you do not know,
  do not invent it. Suggest an honest answer or ask for clarification.
- Keep the reply short, practical, polite, and easy to say aloud.
"""

    return f"""
You are MAY ROGA Live English.

Your purpose is to help a person respond to spoken English during a
real conversation or telephone call. The user will speak the response
themselves. You must provide the words they can say next.

{mode_instructions}

Return valid JSON only with exactly these keys:
"answer": a natural English reply the user can say aloud.
"note": a short English clarification, or an empty string.

RECENT CONVERSATION:
{context or "(No earlier context available)"}

LATEST RECOGNIZED SPEECH:
{transcript}

IMPORTANT RULES:
- Give the proposed reply, not a translation of the latest speech.
- Usually provide 1 to 3 short sentences.
- Do not explain your reasoning or add unnecessary introductions.
- Do not repeat the other person's entire statement.
- Do not claim the suggested answer is what the other person said.
- Do not invent personal facts, promises, qualifications, or commitments.
- If the recognized speech is unclear or incomplete, use "note" to
  briefly explain the uncertainty and suggest asking the speaker to
  repeat or clarify.
- Do not translate into Spanish.
- Do not include Markdown fences or additional JSON keys.
""".strip()


def translation_prompt(transcript: str) -> str:
    return (
        "Translate the following English conversation into natural Spanish. "
        "Preserve the meaning, uncertainty, and order of the text. Do not "
        "invent missing words or add advice. Return only the translation.\n\n"
        + transcript
    )


async def ask_gemini(prompt: str, json_mode: bool = False) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini key is not configured.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )

    generation_config = {
        "temperature": 0.2,
        "maxOutputTokens": 500
    }

    if json_mode:
        generation_config["responseMimeType"] = "application/json"

    response = await app.state.client.post(
        url,
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": generation_config
        }
    )
    response.raise_for_status()
    data = response.json()
    candidates = data.get("candidates") or []

    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    result = "".join(
        part.get("text", "")
        for part in parts
        if isinstance(part, dict)
    ).strip()

    if not result:
        raise RuntimeError("Gemini returned empty text.")

    return result


async def ask_openai(prompt: str, json_mode: bool = False) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OpenAI key is not configured.")

    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "max_output_tokens": 500,
        "store": False
    }

    if json_mode:
        payload["text"] = {
            "format": {"type": "json_object"}
        }

    response = await app.state.client.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    response.raise_for_status()
    data = response.json()

    texts = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                texts.append(part.get("text", ""))

    result = "\n".join(texts).strip()

    if not result:
        raise RuntimeError("OpenAI returned empty text.")

    return result


async def generate(prompt: str, json_mode: bool = False):
    errors = []

    if GEMINI_API_KEY:
        try:
            return await ask_gemini(prompt, json_mode), "Gemini"
        except Exception as exc:
            log.warning("Gemini failed: %s", type(exc).__name__)
            errors.append("Gemini")

    if OPENAI_API_KEY:
        try:
            return await ask_openai(prompt, json_mode), "OpenAI fallback"
        except Exception as exc:
            log.warning("OpenAI fallback failed: %s", type(exc).__name__)
            errors.append("OpenAI")

    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        detail = "Configure GEMINI_API_KEY or OPENAI_API_KEY in Render."
    else:
        detail = (
            "AI services unavailable. Check API keys, quota, model access, "
            "and connection."
        )

    raise HTTPException(status_code=503, detail=detail)


@app.get("/", response_class=HTMLResponse)
async def home():
    candidates = [
        BASE_DIR / "templates" / "index.html",
        BASE_DIR / "index.html"
    ]

    html_file = next(
        (path for path in candidates if path.is_file()),
        None
    )

    if html_file is None:
        log.error("index.html not found in expected locations.")
        raise HTTPException(
            status_code=500,
            detail="index.html not found. Check the application file structure."
        )

    return HTMLResponse(
        html_file.read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-store"}
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY),
        "openai_fallback_configured": bool(OPENAI_API_KEY),
        "response_endpoint": "/api/respond",
        "translation_endpoint": "/api/translate"
    }


@app.post("/api/respond")
async def respond(body: ConversationRequest):
    transcript = body.transcript.strip()
    context = body.context.strip()

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript is empty."
        )

    prompt = response_prompt(
        transcript=transcript,
        context=context,
        mode=body.mode
    )

    raw, provider = await generate(prompt, json_mode=True)
    result = parse_json_response(raw)

    answer = str(result.get("answer", "")).strip()
    note = str(result.get("note", "")).strip()

    if not answer:
        raise HTTPException(
            status_code=502,
            detail="The AI service did not return a usable reply."
        )

    return {
        "answer": answer[:2500],
        "note": note[:500],
        "provider": provider,
        "mode": body.mode
    }


@app.post("/api/translate")
async def translate(body: TranslationRequest):
    transcript = body.transcript.strip()

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript is empty."
        )

    raw, provider = await generate(translation_prompt(transcript))

    return {
        "translation": raw[:15000],
        "provider": provider
    }
