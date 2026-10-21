import os
import json
import logging
import asyncio
import re
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
GEMINI_LIMIT = 4.7
OPENAI_LIMIT = 4.7
AI_TOTAL_LIMIT = 4.9
CONNECT_LIMIT = 1.5

TIMEOUT = httpx.Timeout(
    timeout=8.0,
    connect=CONNECT_LIMIT,
    read=6.0,
    write=3.0,
    pool=1.0
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mayroga.liveenglish")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=TIMEOUT)
    yield
    await app.state.client.aclose()


app = FastAPI(
    title="MAY ROGA Live English",
    version="1.4.0",
    lifespan=lifespan
)


class ConversationRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=MAX_TEXT)
    context: str = Field(default="", max_length=5000)
    mode: str = Field(
        default="conversation",
        pattern="^(conversation|interview)$"
    )
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

    # Try to recover a JSON object if the provider added extra text.
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            value = json.loads(match.group(0))
            if isinstance(value, dict):
                return value
        except (ValueError, TypeError):
            pass

    return {"answer": text[:2500], "note": ""}


def response_prompt(
    transcript: str,
    context: str,
    mode: str,
    style: str = ""
) -> str:
    if mode == "interview":
        mode_instructions = """
You help the user answer job interview questions in spoken English.

Identify the interviewer's latest question and answer that question directly.
Use short, honest, professional answers that are easy to say aloud.
Use known user information only when relevant.
Never invent work experience, achievements, licenses, skills, numbers,
qualifications, salary history, or personal details.
The user has an MBA and experience related to restaurant operations,
air cargo operations, and an independent digital business.
Use those details only when they genuinely fit the question.
Do not claim unprovided results or specialized experience.
For follow-up questions such as "Why?", "How?", "What happened next?",
or "Can you give an example?", use the recent conversation.
If a question asks for a specific personal example that is not known,
give a truthful answer about the user's approach without inventing an event.
If the speaker makes a statement rather than asking a question,
respond naturally and professionally.
"""
    else:
        mode_instructions = """
You help the user take part in a real English conversation or phone call.

Respond naturally to the other person's latest statement or question.
Return words the user can say in reply.
For greetings, greet the person back.
For questions, answer directly if enough information is available.
For requests, respond appropriately or ask a brief clarifying question.
For thanks, apologies, agreement, disagreement, or farewells,
use a natural conversational response.
Use recent conversation to understand short replies and follow-up questions.
Never invent personal information or make commitments for the user.
"""

    return f"""
You are MAY ROGA Live English, a written live-response assistant.

MAIN TASK:
The user hears someone speaking English. You receive the recognized speech
and provide the English words the user can say in response.
The user reads the response and speaks it.
Never speak aloud or return audio.

MODE INSTRUCTIONS:
{mode_instructions}

STRICT ANSWER RULES:
- Use simple, natural US English.
- Prefer common words and short sentences.
- Normally use one or two sentences, maximum 45 words.
- Return the reply itself, not a translation of the question.
- Do not start with "You can say" or "The answer is".
- Do not repeat the entire question.
- Do not include Spanish in the answer.
- Do not invent facts, experience, or commitments.
- If the speech is unclear, say:
  "I'm sorry, could you repeat that, please?"
- If the recognized speech is only a fragment, use context carefully.
- For interview answers, be professional but easy to speak aloud.
- Return valid JSON with exactly two keys:
  "answer": the English words the user can say.
  "note": a short English note if needed, otherwise an empty string.
- Do not use Markdown fences.

ADDITIONAL USER STYLE:
{style or "Use short, clear, easy-to-say English."}

RECENT CONVERSATION:
{context or "(No earlier context available)"}

LATEST RECOGNIZED SPEECH:
{transcript}

Return only valid JSON.
""".strip()


def translation_prompt(transcript: str) -> str:
    return (
        "Translate this English conversation into natural Spanish. "
        "Preserve the original meaning and uncertainty. Do not add advice. "
        "Return only the Spanish translation.\n\n"
        + transcript
    )


async def ask_gemini(prompt: str, json_mode: bool = False) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini key is not configured.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )

    config = {
        "temperature": 0.2,
        "maxOutputTokens": 300
    }

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
        "max_output_tokens": 300,
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

    if response.is_error:
        log.warning("OpenAI HTTP error: %s", response.status_code)
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
    """
    Call configured providers concurrently.
    Gemini has a 3-second limit and OpenAI a 2-second limit.
    Return the first successful result; cancel unfinished tasks afterward.
    """
    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Configure GEMINI_API_KEY or OPENAI_API_KEY in Render."
        )

    tasks = {}

    if GEMINI_API_KEY:
        tasks[
            asyncio.create_task(
                asyncio.wait_for(
                    ask_gemini(prompt, json_mode),
                    timeout=GEMINI_LIMIT
                )
            )
        ] = "Gemini"

    if OPENAI_API_KEY:
        tasks[
            asyncio.create_task(
                asyncio.wait_for(
                    ask_openai(prompt, json_mode),
                    timeout=OPENAI_LIMIT
                )
            )
        ] = "OpenAI"

    pending = set(tasks.keys())
    errors = []
    deadline = asyncio.get_running_loop().time() + AI_TOTAL_LIMIT

    try:
        while pending:
            remaining = max(0.0, deadline - asyncio.get_running_loop().time())
            if remaining <= 0:
                break
            done, pending = await asyncio.wait(
                pending,
                timeout=remaining,
                return_when=asyncio.FIRST_COMPLETED
            )
            if not done:
                break

            # Use the first successful provider; cancel the other request.
            for task in done:
                provider = tasks[task]

                try:
                    result = task.result()
                    if result and result.strip():
                        return result, provider
                    errors.append(f"{provider}: empty response")
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    log.warning(
                        "%s failed or timed out: %s",
                        provider,
                        type(exc).__name__
                    )
                    errors.append(f"{provider}: {type(exc).__name__}")

        raise HTTPException(
            status_code=503,
            detail=(
                "AI services did not respond in time. "
                "Use the prepared question library or try again."
            )
        )

    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*tasks.keys(), return_exceptions=True)


def local_fallback(
    transcript: str,
    context: str = "",
    mode: str = "conversation"
) -> str:
    """
    Fast response used when the AI providers fail or time out.
    This is a fallback, not a substitute for the prepared HTML library.
    """
    text = re.sub(r"\s+", " ", transcript or "").strip().lower()

    if not text:
        return "I'm sorry, could you repeat that, please?"

    if re.search(r"\b(hello|hi|hey|good morning|good afternoon)\b", text):
        return "Hello. It's nice to speak with you."

    if re.search(r"\b(thank you|thanks|many thanks)\b", text):
        return "You're welcome."

    if re.search(r"\b(nice to meet you|pleased to meet you)\b", text):
        return "It's nice to meet you, too."

    if re.search(r"\b(how are you|how's it going)\b", text):
        return "I'm doing well, thank you. How are you?"

    if re.search(r"\b(could you repeat|say that again|didn't hear)\b", text):
        return "Of course. Could you please repeat that?"

    if mode == "interview":
        if re.search(
            r"\b(tell me about yourself|introduce yourself)\b",
            text
        ):
            return (
                "I have an MBA and experience in operations, customer service, "
                "and air cargo activities. I am interested in using my "
                "management and problem-solving skills to support a team."
            )

        if re.search(r"\b(your strengths|what are your strengths)\b", text):
            return (
                "My strengths are organization, responsibility, and "
                "problem-solving. I focus on following procedures, "
                "communicating clearly, and completing tasks carefully."
            )

        if re.search(r"\b(why should we hire you|why hire you)\b", text):
            return (
                "I bring an MBA, practical operations experience, and a "
                "willingness to learn. I take responsibilities seriously "
                "and work to support the team's goals."
            )

        if re.search(r"\b(why this job|why this position|why do you want)\b", text):
            return (
                "This position interests me because it fits my background "
                "and gives me an opportunity to contribute, learn, "
                "and grow professionally."
            )

        if re.search(r"\b(weakness|area to improve)\b", text):
            return (
                "I am continuing to improve my professional English. "
                "I practice regularly and focus on communicating clearly "
                "and confidently."
            )

        if re.search(r"\b(any questions for us|questions for me)\b", text):
            return (
                "Yes, thank you. What would be the main priorities for "
                "the person in this position during the first 90 days?"
            )

        return (
            "That is a good question. I would review the requirements, "
            "consider the available information, and choose a practical "
            "solution while following the relevant procedures."
        )

    # General conversation fallback.
    if re.search(r"\b(can you help|could you help)\b", text):
        return "Of course. Could you tell me a little more about what you need?"

    if re.search(r"\b(sorry|i apologize|my apologies)\b", text):
        return "No problem. Thank you for letting me know."

    if re.search(r"\b(goodbye|bye|see you later)\b", text):
        return "Goodbye. Have a great day."

    # Use context as a cue, but do not fabricate a specific answer.
    if context.strip():
        return "I understand. Could you tell me a little more about that?"

    return "I'm sorry, could you repeat that, please?"


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
            detail=(
                "index.html not found. Check that it exists in "
                "the templates folder or application root."
            )
        )

    return HTMLResponse(
        html_file.read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-store"}
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": "MAY ROGA Live English",
        "version": app.version,
        "gemini_configured": bool(GEMINI_API_KEY),
        "openai_fallback_configured": bool(OPENAI_API_KEY),
        "gemini_timeout_seconds": GEMINI_LIMIT,
        "openai_timeout_seconds": OPENAI_LIMIT,
        "total_ai_timeout_seconds": AI_TOTAL_LIMIT,
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
        mode=body.mode,
        style=body.response_style
    )

    try:
        raw, provider = await generate(prompt, json_mode=True)
        result = parse_json_response(raw)

        answer = str(result.get("answer", "")).strip()
        note = str(result.get("note", "")).strip()

        if not answer:
            raise ValueError("The AI response did not contain an answer.")

        return {
            "answer": answer[:1200],
            "note": note[:300],
            "provider": provider,
            "source": "AI",
            "mode": body.mode,
            "fallback": False
        }

    except Exception as exc:
        if isinstance(exc, HTTPException):
            log.warning("Using local response: %s", exc.detail)
        else:
            log.warning(
                "Response generation failed: %s",
                type(exc).__name__
            )

        answer = local_fallback(
            transcript=transcript,
            context=context,
            mode=body.mode
        )

        return {
            "answer": answer,
            "note": "Prepared fallback response. AI was unavailable or too slow.",
            "provider": "Respuesta local de respaldo",
            "source": "Local fallback",
            "mode": body.mode,
            "fallback": True
        }


@app.post("/api/translate")
async def translate(body: TranslationRequest):
    transcript = body.transcript.strip()

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript is empty."
        )

    prompt = translation_prompt(transcript)

    try:
        raw, provider = await generate(prompt)
        return {
            "translation": raw[:15000],
            "provider": provider
        }
    except HTTPException:
        raise
    except Exception as exc:
        log.warning("Translation failed: %s", type(exc).__name__)
        raise HTTPException(
            status_code=503,
            detail="Translation is temporarily unavailable. Please try again."
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
