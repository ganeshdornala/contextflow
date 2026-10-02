import os
import httpx
import json

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:1.7b",
)

SYSTEM_PROMPT="""
You are ContextFlow, a concise and helpful AI assistant.
Rules:
- Answer directly.
- Be concise.
- Do not repeat the user's question.
- Do not add unnecessary explanations.
- Follow the requested format exactly.
"""

async def generate_response(prompt:str)->str:
    payload={
        "model":MODEL_NAME,
        "system":SYSTEM_PROMPT,
        "prompt":prompt,
        "stream":False,
        "think":False,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response=await client.post(
                OLLAMA_URL,
                json=payload,
            )
            response.raise_for_status()
            data=response.json()
            return data["response"]
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI model took too long to respond.",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI model is unavailable.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI response.",
        )

async def generate_json(prompt:str)->dict:
    payload={
        "model":MODEL_NAME,
        "system":SYSTEM_PROMPT,
        "prompt":prompt,
        "stream":False,
        "think":False,
        "format":"json",
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return json.loads(data["response"])
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI model took too long to respond.",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI model is unavailable.",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="AI model returned invalid JSON.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI response.",
        )

async def stream_response(prompt:str):
    payload={
        "model":MODEL_NAME,
        "system":SYSTEM_PROMPT,
        "prompt":prompt,
        "stream":True,
        "think":False,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    data=json.loads(line)
                    if data.get("response"):
                        yield data["response"]
                    if data.get("done"):
                        break