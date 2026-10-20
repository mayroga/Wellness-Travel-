
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
TIMEOUT = httpx.Timeout(35.0, connect=10.0)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mayroga.liveenglish")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=TIMEOUT)
    yield
    await app.state.client.aclose()


app = FastAPI(
    title="MAY ROGA Live English",
    version="1.3.0",
    lifespan=lifespan
)


class ConversationRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)
    context: str = Field(default="", max_length=5000)
    mode: str = Field(default="conversation", pattern="^(conversation|interview)$")
    response_style: str = Field(default="", max_length=3000)
    language: str = Field(default="en-US", max_length=20)
    automatic: bool = False


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


def response_prompt(transcript: str, context: str, mode: str, style: str = "") -> str:
    if mode == "interview":
        mode_instructions = """
You help the user answer job interview questions in spoken English.
Identify what the interviewer actually asks and answer that question.
Use short, honest, professional answers with common words.
Use the user's known context when relevant, but never invent facts.
For unknown personal details, give a safe honest answer or ask for clarification.
If asked about experience, skills, education, salary, or availability, do not
claim details that the user has not provided.
If the speaker makes a statement rather than asking a question, respond naturally.
"""
    else:
        mode_instructions = """
You help the user take part in a real English conversation or phone call.
Reply to the latest statement or question as a person would.
For greetings, greet the person back.
For a question, answer it directly if enough information is available.
For a request, give a suitable reply or ask a short clarifying question.
For thanks, apologize, agreement, or a farewell, respond naturally.
Use the recent conversation to understand short replies and follow-up questions.
Never invent the user's personal information or make commitments for them.
"""

    return f"""
You are MAY ROGA Live English, a written live-response assistant.

MAIN TASK:
The user hears another person speaking English. You read the recognized words
and provide the exact simple English words the user can say in reply.
The user will read the answer and speak it. Do not speak aloud.

{mode_instructions}

STRICT ANSWER RULES:
- Write in simple, natural US English.
- Prefer common words and short sentences.
- Normally use one or two sentences, maximum 45 words.
- Give the reply itself, not a translation of the other person's words.
- Do not start with "You can say", "The answer is", or explanations.
- No difficult synonyms, long introductions, or unnecessary details.
- Do not include Spanish in the answer.
- Do not repeat the full question.
- If the speech is unclear, suggest a short phrase such as:
  "I'm sorry, could you repeat that, please?"
- If the words are only a fragment, use the context and avoid guessing too much.
- Return JSON only with exactly two keys:
  "answer": the words the user can say in English.
  "note": a brief English note only when needed; otherwise an empty string.

ADDITIONAL USER STYLE:
{style or "Use short, clear, easy-to-say English."}

RECENT CONVERSATION:
{context or "(No earlier context available)"}

LATEST RECOGNIZED SPEECH:
{transcript}

Return only valid JSON. No Markdown fences.
""".strip()


def translation_prompt(transcript: str) -> str:
    return (
        "Translate this English conversation into natural Spanish. "
        "Keep the original meaning and uncertainty. Do not add advice. "
        "Return only the Spanish translation.\n\n" + transcript
    )


async def ask_gemini(prompt: str, json_mode: bool = False) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini key is not configured.")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    config = {"temperature": 0.2, "maxOutputTokens": 300}
    if json_mode:
        config["responseMimeType"] = "application/json"
    response = await app.state.client.post(
        url,
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": config
        }
    )
    if response.is_error:
        log.warning("Gemini HTTP error: %s", response.status_code)
        response.raise_for_status()
    data = response.json()
    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")
    parts = candidates[0].get("content", {}).get("parts", [])
    result = "".join(
        part.get("text", "")
        for part in parts if isinstance(part, dict)
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
        "max_output_tokens": 300,
        "store": False
    }
    if json_mode:
        payload["text"] = {"format": {"type": "json_object"}}
    response = await app.state.client.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    if response.is_error:
        log.warning("OpenAI HTTP error: %s", response.status_code)
        response.raise_for_status()
    data = response.json()
    texts = []
    for item in data.get("output", []):
        if item.get("type") == "message":
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
            "model names, and connection."
        )
    raise HTTPException(status_code=503, detail=detail)


@app.get("/", response_class=HTMLResponse)
async def home():
    candidates = [
        BASE_DIR / "templates" / "index.html",
        BASE_DIR / "index.html"
    ]
    html_file = next((path for path in candidates if path.is_file()), None)
    if html_file is None:
        log.error("index.html not found.")
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
        raise HTTPException(status_code=400, detail="Transcript is empty.")
    prompt = response_prompt(
        transcript=transcript,
        context=context,
        mode=body.mode,
        style=body.response_style
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
        "answer": answer[:1200],
        "note": note[:300],
        "provider": provider,
        "mode": body.mode
    }


@app.post("/api/translate")
async def translate(body: TranslationRequest):
    transcript = body.transcript.strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript is empty.")
    raw, provider = await generate(translation_prompt(transcript))
    return {
        "translation": raw[:15000],
        "provider": provider
    }
