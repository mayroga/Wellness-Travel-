
import os
import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, ConfigDict

BASE_DIR = Path(__file__).resolve().parent
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
MAX_TEXT = 10000
MAX_CONTEXT = 5000
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
    model_config = ConfigDict(extra="ignore")
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)
    context: str = Field(default="", max_length=MAX_CONTEXT)
    mode: str = Field(default="conversation", max_length=30)


class CorrectionRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)
    context: str = Field(default="", max_length=MAX_CONTEXT)


class TranslationRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
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
    return {}


def response_prompt(transcript: str, context: str, mode: str) -> str:
    if mode == "interview":
        role = """
MODE: INTERVIEW / QUESTIONS AND ANSWERS.
Identify the latest question and answer that question directly.
Keep the answer relevant to the exact question and professional context.
Use natural, complete English sentences that are easy to read.
Do not invent the user's experience, education, qualifications, achievements,
employment history, personal opinions, promises, dates, or other personal facts.
If the answer requires personal information not provided, offer a truthful
answer framework or a polite way to clarify instead of inventing details.
If the speech is an instruction rather than a question, respond appropriately.
"""
    else:
        role = """
MODE: REAL CONVERSATION.
Respond naturally to the latest recognized speech and the conversation context.
Stay on the same subject. Match the speaker's meaning, tone, and purpose.
Do not introduce unrelated topics, unnecessary questions, stories, facts,
advice, or vocabulary that does not belong in the conversation.
For greetings, respond to the greeting. For questions, answer the question.
For instructions, acknowledge or clarify the instruction as appropriate.
Never invent personal information about the user.
"""

    return f"""
You are MAY ROGA Live English. Help the user understand English and prepare
a written reply that the user will speak themselves.

{role}

STRICT RULES:
1. Return valid JSON only, with exactly these keys:
   "answer": complete English reply suitable for the situation.
   "note": brief English clarification, or an empty string.
2. Keep every sentence complete. Never cut off a sentence or leave a
   thought unfinished. Usually use 1 to 3 complete sentences.
3. Every word and sentence must be relevant to the latest speech and topic.
   Do not add unrelated content, filler, invented dialogue, or explanations.
4. Use the recent context only to understand the current topic. Respond
   primarily to the latest recognized speech.
5. The recognized transcript may contain errors. Infer a missing or unclear
   word only when the surrounding words and context strongly support one
   interpretation. Never invent missing speech or claim uncertain words
   are certain.
6. If a missing word changes the meaning or cannot be recovered reliably,
   say so briefly in "note" and suggest a concise, relevant request for
   repetition or clarification. Do not fabricate an answer based on a guess.
7. If the latest speech is too incomplete to answer, suggest a polite,
   context-appropriate clarification in English.
8. For interview questions requiring personal details, never make up
   the user's background or experience. Give a truthful response framework
   or suggest how to clarify what is being asked.
9. Do not translate into Spanish in the answer.
10. Do not output Markdown fences, extra JSON keys, or commentary outside JSON.

RECENT CONVERSATION:
{context or "(No previous context available)"}

LATEST RECOGNIZED SPEECH:
{transcript}
""".strip()


def correction_prompt(transcript: str, context: str) -> str:
    return f"""
You are checking an English speech-recognition transcript.
Your task is to correct recognition errors, not to rewrite the speaker.

Return valid JSON only with exactly these keys:
"corrected": corrected English transcript.
"note": a brief uncertainty note, or an empty string.

RECENT CONTEXT:
{context or "(No context available)"}

RECOGNIZED TRANSCRIPT:
{transcript}

Rules:
- Preserve the original meaning, order, and complete sentences.
- Correct spelling, punctuation, and obvious speech-recognition errors.
- Use context to infer an omitted or misheard word only when the evidence
  strongly supports the correction.
- Never add a new idea, sentence, claim, answer, or topic.
- Never fill a gap merely because a particular word would sound natural.
- If a word cannot be recovered reliably, preserve the available words
  and identify the uncertainty in "note".
- Do not turn a guess into a confirmed statement.
- Return the corrected transcript in English, without translation.
""".strip()


def translation_prompt(transcript: str) -> str:
    return (
        "Translate the following English transcript into natural Spanish. "
        "Preserve the meaning, order, and uncertainty. Do not add ideas, "
        "complete missing speech by guessing, or give advice. Return only "
        "the Spanish translation.\n\n" + transcript
    )


async def ask_gemini(prompt: str, json_mode: bool = False) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini key is not configured.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    config = {"temperature": 0.1, "maxOutputTokens": 900}
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
        "max_output_tokens": 900,
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
    if GEMINI_API_KEY:
        try:
            return await ask_gemini(prompt, json_mode), "Gemini"
        except Exception as exc:
            log.warning("Gemini request failed: %s", type(exc).__name__)

    if OPENAI_API_KEY:
        try:
            return await ask_openai(prompt, json_mode), "OpenAI fallback"
        except Exception as exc:
            log.warning("OpenAI request failed: %s", type(exc).__name__)

    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        detail = "Configure GEMINI_API_KEY or OPENAI_API_KEY in Render."
    else:
        detail = (
            "AI services are unavailable. Check API keys, quota, model "
            "access, and connection."
        )
    raise HTTPException(status_code=503, detail=detail)


def safe_string(value, limit: int) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()[:limit]


@app.get("/", response_class=HTMLResponse)
async def home():
    html_file = BASE_DIR / "index.html"
    if not html_file.is_file():
        raise HTTPException(status_code=500, detail="index.html not found.")
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
        "speech_correction_available": bool(
            GEMINI_API_KEY or OPENAI_API_KEY
        )
    }


@app.post("/api/respond")
async def respond(body: ConversationRequest):
    transcript = body.transcript.strip()
    context = body.context.strip()
    mode = body.mode.strip().lower()

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript is empty.")
    if mode not in {"conversation", "interview"}:
        mode = "conversation"

    prompt = response_prompt(transcript, context, mode)
    raw, provider = await generate(prompt, json_mode=True)
    result = parse_json_response(raw)

    answer = safe_string(result.get("answer"), 2500)
    note = safe_string(result.get("note"), 500)

    if not answer:
        raise HTTPException(
            status_code=502,
            detail="The AI service did not return a usable reply."
        )

    return {
        "answer": answer,
        "note": note,
        "provider": provider,
        "mode": mode
    }


@app.post("/api/correct")
async def correct_transcript(body: CorrectionRequest):
    transcript = body.transcript.strip()
    context = body.context.strip()

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript is empty.")

    prompt = correction_prompt(transcript, context)
    raw, provider = await generate(prompt, json_mode=True)
    result = parse_json_response(raw)

    corrected = safe_string(result.get("corrected"), MAX_TEXT)
    note = safe_string(result.get("note"), 500)

    if not corrected:
        raise HTTPException(
            status_code=502,
            detail="The AI service did not return a corrected transcript."
        )

    return {
        "corrected": corrected,
        "note": note,
        "provider": provider
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
