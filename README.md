# ContextFlow

ContextFlow is a local AI productivity assistant that transforms unstructured text into useful outputs such as summaries, professional rewrites, structured information, and generated content.

It uses a React + TypeScript frontend, a FastAPI backend, and a locally running Qwen3 language model through Ollama.

## Features

- Conversational chat with context
- Streaming AI responses
- Text summarization
- Professional rewriting
- Structured JSON extraction
- Content generation
- Backend error handling
- Local LLM execution

## Architecture

```text
React + TypeScript
        |
        | HTTP
        v
     FastAPI
        |
        v
      Ollama
        |
        v
   Qwen3 1.7B
```

## Tech Stack

### Frontend

- React
- TypeScript
- Vite

### Backend

- Python
- FastAPI
- HTTPX
- Pytest

### AI

- Ollama
- Qwen3 1.7B

## Why Local LLM?

ContextFlow runs the model locally through Ollama, so the application does not require a paid cloud LLM API or an API key for development.

## Project Structure

```text
contextflow/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── services/
│   │       └── llm.py
│   ├── tests/
│   │   └── test_routes.py
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── App.tsx
│       └── index.css
│
└── README.md
```

## Running Locally

### 1. Start Ollama

Make sure Ollama is installed and the Qwen3 model is available:

```bash
ollama list
```

The application expects:

```text
qwen3:1.7b
```

If it is missing, pull it with:

```bash
ollama pull qwen3:1.7b
```

### 2. Start the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Testing

Backend tests:

```bash
cd backend
source .venv/bin/activate
pytest -v
```

## API Endpoints

```text
POST /chat
POST /chat/stream
POST /summarize
POST /rewrite
POST /extract
POST /generate
GET  /health
```

## Key LLM Concepts Demonstrated

- Prompt engineering
- System prompts
- Conversation context
- Structured JSON output
- Streaming generation
- Local model integration
- Error handling
- Model configuration