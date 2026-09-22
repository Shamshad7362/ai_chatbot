# AI Chatbot

A lightweight web chatbot built with Python, Flask, and the OpenRouter chat-completions API. It keeps the current conversation in memory and renders assistant responses as Markdown, including tables and fenced code blocks.

## Features

- Chat interface with conversation history for the active server session
- OpenRouter-powered assistant responses
- Markdown rendering with table, code-fence, and syntax-highlighting support
- Responsive dark chat interface

## Project structure

```text
ai-chatbot/
├── backend/
│   ├── app.py          # Flask routes and page rendering
│   ├── ai_service.py   # OpenRouter client and conversation state
│   └── config.py       # Loads environment configuration
├── frontend/
│   ├── index.html      # Chat UI template
│   └── assets/
│       ├── style.css   # Dark-mode UI styles
│       └── script.js   # Frontend scripts
├── .env                # Local API key (do not commit)
└── requirements.txt
```

## Prerequisites

- Python 3.10 or later
- An [OpenRouter API key](https://openrouter.ai/keys)

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On Command Prompt, use `.venv\Scripts\activate.bat` instead.

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   pip install flask pygments
   ```

   `flask` and `pygments` are used by the current backend but are not yet listed in `requirements.txt`.

3. Create a `.env` file in the project root:

   ```env
   OPEN_ROUTERAI_API_KEY=your_openrouter_api_key
   ```

## Run the app

From the project root, run:

```powershell
python backend/app.py
```

Open the address printed by Flask—normally [http://127.0.0.1:5000](http://127.0.0.1:5000)—in your browser.

## How it works

1. The page submits the prompt to `POST /ask`.
2. `Chatbot.ask()` sends the full in-memory conversation to OpenRouter.
3. The backend converts assistant Markdown to HTML and re-renders the conversation.

Conversation history is stored only in the running Python process, so it resets whenever the server restarts.

## Configuration

The default model is configured in `backend/ai_service.py`:

```python
model="inclusionai/ling-3.0-flash-vl:free"
```

Replace it with an OpenRouter model available to your account if needed.

## Security note

Keep `.env` private and never commit your API key. The app renders assistant Markdown as HTML; if you later display untrusted content, sanitize it before rendering.
