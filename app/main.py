import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .tools import calculate, get_current_datetime, convert_units, convert_currency

load_dotenv()

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(APP_DIR), "static")

app = FastAPI(title="Aiva AI Assistant", version="2.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
SYSTEM_PROMPT = os.getenv(
    "ASSISTANT_SYSTEM_PROMPT",
    "You are Aiva, a helpful AI personal assistant. "
    "Be concise, practical, friendly, and honest. "
    "Use the available tools whenever they are appropriate. "
    "Use the calculator for mathematical calculations. "
    "Use the date/time tool whenever the user asks for the current date or time. "
    "Use the unit converter for supported unit conversions. "
    "Use the currency converter whenever the user asks to convert one currency into another. "
    "Use currency codes such as USD, INR, EUR, GBP, and JPY when calling the currency converter. "
    "Tell the user the rate date because exchange rates are updated periodically, not continuously. "
    "Never invent a tool result. "
    "After using a tool, explain the result clearly to the user."
)


client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
    except ImportError:
        client = None


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=12000)


class ChatRequest(BaseModel):
    messages: List[Message] = Field(min_length=1, max_length=30)


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "ai_configured": bool(GEMINI_API_KEY and client),
        "provider": "Google Gemini",
        "model": MODEL,
    }


def _build_contents(messages: List[Message]):
    # Gemini's content roles use "user" and "model". Aiva stores the assistant side as "assistant".
    return [
        {"role": "user" if message.role == "user" else "model", "parts": [{"text": message.content}]}
        for message in messages
    ]


@app.post("/api/chat")
def chat(request: ChatRequest):
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Create a Gemini API key and add GEMINI_API_KEY.",
        )

    try:
        from google.genai import types

        response = client.models.generate_content(
    model=MODEL,
    contents=_build_contents(request.messages),
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[
            calculate,
            get_current_datetime,
            convert_units,
            convert_currency,
        ],
    ),
)
        text = (response.text or "").strip()
        if not text:
            raise HTTPException(status_code=502, detail="The AI returned an empty response.")
        return {"reply": text}
    except HTTPException:
        raise
    except Exception as exc:
        # Keep provider internals and credentials out of the browser response.
        print(f"Gemini request failed: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=502, detail="The AI service could not complete the request.") from exc
