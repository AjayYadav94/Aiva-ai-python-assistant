# Aiva — AI Python Assistant (Free-Tier Edition)

A portfolio-ready AI assistant built with **Python + FastAPI + Google Gemini + browser voice APIs**. It is packaged for **Docker** and can be deployed to free hosting for a public demo.

## What is free?

This version no longer uses the paid OpenAI API. It uses the **Gemini API** with a model that currently has a free tier. Google currently lists `gemini-2.5-flash-lite` with free input/output pricing for the Gemini API. Free-tier availability and quotas can change, so check Google's current pricing page before relying on it for heavy traffic. citeturn213164search11turn213164search13

For the API key, use Google AI Studio and store the key in `GEMINI_API_KEY`. Google's current documentation recommends environment variables for API keys. citeturn213164search1turn213164search9

## Features

- AI conversational assistant through a FastAPI backend
- Multi-turn conversation history in the browser
- Voice input using the browser Speech Recognition API when supported
- Voice output using browser speech synthesis
- Responsive web interface
- Health endpoint for deployment checks
- Environment-variable based secret management
- Dockerized for local or cloud deployment
- No OpenAI billing required

## Run locally on Windows

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Put your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

Then start the server:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/api/health
- http://127.0.0.1:8000/docs

## Get a free Gemini API key

Google's current Gemini getting-started flow allows you to create an API key in Google AI Studio and use the free tier. The paid tier is a separate upgrade that requires billing. citeturn213164search6turn213164search9

## Docker

```bash
docker build -t aiva-ai-assistant .
docker run --rm -p 8080:8080 --env-file .env aiva-ai-assistant
```

## Free live demo

A simple path for a portfolio demo is a free web-service host such as Render. Render documents a free tier for web services, with the limitation that free services spin down after periods of inactivity and may take about a minute to wake. citeturn145980search0

Recommended deployment settings:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Add this environment variable in the hosting dashboard:

```text
GEMINI_API_KEY=<your key>
GEMINI_MODEL=gemini-2.5-flash-lite
```

## Architecture

```text
Browser
  ├── Speech Recognition ──> typed prompt
  ├── Chat UI              ──> POST /api/chat
  └── Speech Synthesis     <── AI response

                 FastAPI / Python
                       |
                Google Gemini API
                       |
             gemini-2.5-flash-lite
```

## Resume-ready project description

**Aiva — AI Python Assistant** | Python, FastAPI, Google Gemini, JavaScript, Docker

- Built a web-based AI assistant with a Python/FastAPI backend and multi-turn conversational memory.
- Integrated browser speech recognition and text-to-speech for hands-free interaction.
- Implemented environment-based secret management, health checks, automated tests, and Docker deployment support.
