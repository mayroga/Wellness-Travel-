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

    return f
You are MAY ROGA Live English, a written live-response assistant.

MAIN TASK:
The user hears another person speaking English. You read the recognized words
and provide the exact simple English words the user can say in reply.
The user will read the answer and speak it. Do not speak aloud.

{mode_instructions}
