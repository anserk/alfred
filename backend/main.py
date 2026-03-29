# from models import ModelListResponse, RunningResponse
import requests

# import uuid
import json
# import argparse

import logging
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://192.168.1.154:11435/v1/chat/completions"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    model: str | None
    temperature: float | None


def stream_llm(prompt: str, model: str | None = "", temperature: float | None = 0.9):
    logger.info("Sending request to %s", BASE_URL)

    payload = {
        "model": "qwen3.5-9B",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "chat_template_kwargs": {"enable_thinking": False},
        "stream": True,
        "temperature": 0.9,
    }

    try:
        response = requests.post(BASE_URL, json=payload, stream=True, timeout=30)
        logger.info("LLM status: %s", response.status_code)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        logger.error("Connection error: %s", e)
        yield "error: could not connect to model server"
        return
    except requests.exceptions.Timeout:
        logger.error("LLM server timed out")
        yield "error: model server timed out"
        return
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error: %s - %s", e.response.status_code, e.response.text)
        yield f"error: model server returned {e.response.status_code}"
        return

    for line in response.iter_lines():
        if not line:
            continue

        decoded = line.decode("utf-8")

        if not decoded.startswith("data: "):
            continue

        data_str = decoded[6:]

        if data_str == "[DONE]":
            break

        data = json.loads(data_str)

        delta = data["choices"][0]["delta"].get("content")

        if delta:
            yield delta


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(
        stream_llm(req.message, req.model, req.temperature),
        media_type="text/plain",
    )
