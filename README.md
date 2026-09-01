# Aiva — AI Python Assistant

Aiva is a web-based AI personal assistant built with **Python, FastAPI, Google Gemini, and browser speech APIs**. It combines conversational AI with practical Python tools such as calculations, date/time, unit conversion, currency conversion, and web search.

## 🚀 Live Demo

**Live Demo:** https://aiva-ai-python-assistant.onrender.com

**GitHub:** https://github.com/AjayYadav94/aiva-ai-python-assistant

> The live deployment runs the same application hosted from this repository.

## ✨ Features

- 🤖 AI conversations powered by Google Gemini
- 🔧 AI tool/function calling
- 🧮 Safe mathematical calculator
- 🕐 Current date and time
- 📏 Unit conversion
- 💱 Currency conversion using exchange-rate data
- 🔎 Web search with source URLs
- 🎙️ Browser-based voice input
- 🔊 Text-to-speech responses
- 🎚️ Voice selection and speech-speed control
- 🛑 Stop-speaking control
- 💬 Multi-turn conversation history in the browser
- ❤️ Health-check endpoint for deployment monitoring
- 🧪 Automated tests with Pytest
- 🐳 Docker support
- ☁️ Cloud deployment with Render
- 🔐 API keys stored through environment variables

## 🧠 How It Works

```text
User
  │
  ▼
Aiva Web UI
  │
  │ POST /api/chat
  ▼
FastAPI Backend
  │
  ├── Gemini AI ───────────────┐
  │                            │
  ├── Calculator               │
  ├── Date / Time              │
  ├── Unit Converter            │
  ├── Currency Converter       │
  └── Web Search               │
                               ▼
                         Final AI Response
                               │
                               ▼
                         Browser / Voice
```

Gemini handles the natural-language interaction and selects appropriate tools. Python performs the actual calculations and external-service operations.

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| AI | Google Gemini API |
| Frontend | HTML, CSS, JavaScript |
| Voice Input | Browser Speech Recognition API |
| Voice Output | Browser Speech Synthesis API |
| External Services | Frankfurter, Tavily |
| Testing | Pytest |
| Containerization | Docker |
| Version Control | Git / GitHub |
| Deployment | Render |

## 📁 Project Structure

```text
ai_python_assistant/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and Gemini integration
│   └── tools.py         # Python tools used by the assistant
├── static/
│   └── index.html       # Web UI and browser-side JavaScript
├── tests/
│   └── test_health.py   # Health endpoint test
├── .env.example         # Environment-variable template
├── .gitignore
├── .dockerignore
├── Dockerfile
├── deploy.sh
├── requirements.txt
└── README.md
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/AjayYadav94/aiva-ai-python-assistant.git
cd aiva-ai-python-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file:

```powershell
copy .env.example .env
```

Then set your keys in `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit `.env` to GitHub.** The real API keys should stay in your local environment or your cloud provider's secret/environment-variable settings.

### 5. Start the application

```powershell
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000` — Aiva web interface
- `http://127.0.0.1:8000/api/health` — health check
- `http://127.0.0.1:8000/docs` — FastAPI API documentation

## 🔧 Available Tools

### Calculator

Runs mathematical expressions safely in Python instead of asking the LLM to perform the arithmetic itself.

Example:

```text
Calculate 245 * 37
```

### Date & Time

Returns the current server date and time.

Example:

```text
What is the current date and time?
```

### Unit Conversion

Supports common conversions such as distance, weight, and temperature.

Example:

```text
Convert 10 kilometers to miles
```

### Currency Conversion

Uses exchange-rate data from Frankfurter and performs the conversion in Python.

Example:

```text
Convert 1000 USD to INR
```

The response includes the exchange rate and rate date.

### Web Search

Uses Tavily to retrieve web results for current or externally verifiable questions.

Example:

```text
What are the latest AI news headlines today?
```

The assistant can include source URLs so users can inspect the referenced pages.

## 🎙️ Voice Features

Aiva uses browser speech APIs for voice interaction.

- Click the microphone to provide voice input.
- Responses can be spoken aloud.
- Choose an available browser voice.
- Adjust the speech speed.
- Stop speech immediately with the **Stop Speaking** control.

Available voices depend on the user's browser and operating system.

## 🧪 Testing

Run the automated tests with:

```powershell
python -m pytest
```

The test suite currently verifies that the FastAPI health endpoint is available and returns a healthy status.

## 🐳 Docker

Build the image:

```bash
docker build -t aiva-ai-assistant .
```

Run it:

```bash
docker run --rm -p 8080:8080 --env-file .env aiva-ai-assistant
```

Then open:

`http://127.0.0.1:8080`

## ☁️ Deployment

The application is configured for cloud deployment and is currently hosted on Render.

Typical Render settings:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables on the hosting platform:

```text
GEMINI_API_KEY
GEMINI_MODEL
TAVILY_API_KEY
```


## 🔐 Security Notes

- API keys are loaded from environment variables.
- `.env` is excluded from version control.
- API credentials are never hard-coded in the frontend.
- Provider errors are not exposed directly to browser users.

## 📡 API Endpoints

### `GET /`

Serves the Aiva web application.

### `GET /api/health`

Returns application and AI configuration status.

### `POST /api/chat`

Accepts conversation messages and returns the assistant's response.

Example request shape:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Explain Docker in simple terms."
    }
  ]
}
```

## 📸 Screenshots

### Aiva Homepage
![Aiva Homepage](Screenshot%20homepage.png)

### Web Search
![Aiva Web Search](Screenshot%20web%20search.png)

### Source Links
![Aiva Source Links](Screenshot%20source%20url.png)

## 🎯 Why I Built This

This project was built to explore practical AI application development beyond a basic chatbot. It demonstrates how an LLM can be combined with a Python backend, deterministic tools, external APIs, browser capabilities, automated testing, Docker, and cloud deployment.

## 👨‍💻 Author

**Ajay Kumar Yadav**

GitHub: https://github.com/AjayYadav94
