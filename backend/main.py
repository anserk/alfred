# from models import ModelListResponse, RunningResponse
from typing import Optional, List, Any
from models.message import Message
from repositories.message_repository import MessageRepository
from dependencies import get_message_repo

# import uuid
import json
# import argparse

import logging
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncpg
from alembic.config import Config
from contextlib import asynccontextmanager
import os
import httpx
from tools.registry import TOOLS
from tools.executor import execute_tool

alembic_cfg = Config("alembic.ini")
DATABASE_URL = os.environ["DATABASE_URL"]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = os.environ["BASE_URL"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=2,
        max_size=10,
    )
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    conversation_id: str | None = "f7d2e57d-e3cd-4a7c-ae71-b66a56b8ef5f"
    message: str
    model: str | None = None
    temperature: float | None = None


class LLMMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_call_id: Optional[str] = None


def build_messages(
    history: list[Message], max_messages: int = 10000
) -> list[LLMMessage]:

    recent_history = history[-max_messages:]
    return [LLMMessage(role=m.role, content=m.content) for m in recent_history]


async def stream_llm(
    model: str | None = "",
    temperature: float | None = 0.9,
    messages: list[LLMMessage] | None = [],
):
    logger.info("Sending request to %s", BASE_URL)

    payload = {
        "model": "qwen3.5-9B",
        "messages": [m.model_dump(exclude_none=True) for m in messages or []],
        "chat_template_kwargs": {"enable_thinking": False},
        "stream": False,
        "temperature": 0.9,
        "tools": TOOLS,
    }

    if messages is None:
        messages = []

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(BASE_URL, json=payload)
        response = r.json()
        logger.debug("LLM raw response: %s", json.dumps(response, indent=2))

    message = response["choices"][0]["message"]

    if not message.get("tool_calls"):
        yield message["content"]
        return

    tool_call = message["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_inputs = json.loads(tool_call["function"]["arguments"])

    logger.info("Tool call: %s with %s", tool_name, tool_inputs)

    tool_result = await execute_tool(tool_name, tool_inputs)

    messages = (messages or []) + [
        LLMMessage(
            role="assistant",
            tool_calls=[tool_call],
        ),
        LLMMessage(
            role="tool",
            tool_call_id=tool_call["id"],
            content=tool_result,
        ),
    ]

    payload["messages"] = [m.model_dump(exclude_none=True) for m in messages]
    payload["stream"] = True
    payload.pop("tools")

    async with httpx.AsyncClient(timeout=30) as client:
        async with client.stream("POST", BASE_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                data = json.loads(data_str)
                delta = data["choices"][0]["delta"].get("content")
                if delta:
                    yield delta


@app.post("/chat/stream")
async def chat_stream(
    req: ChatRequest, repo: MessageRepository = Depends(get_message_repo)
):

    await repo.add(req.conversation_id or "", "user", req.message)
    history = await repo.list_all()

    messages = build_messages(history)

    async def generate_and_save():
        full_response = []
        async for chunk in stream_llm(req.model, req.temperature, messages):
            full_response.append(chunk)
            yield chunk
        # Save after stream completes
        await repo.add(req.conversation_id or "", "assistant", "".join(full_response))

    return StreamingResponse(
        generate_and_save(),
        media_type="text/plain",
    )
