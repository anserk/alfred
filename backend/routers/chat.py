import json
from services.chat import ChatService
from dependencies import get_chat_service, get_title_queue
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from fastapi.sse import EventSourceResponse, ServerSentEvent
import asyncio
from fastapi.responses import StreamingResponse

router = APIRouter()


class ChatRequest(BaseModel):
    topic_id: str | None = "f7d2e57d-e3cd-4a7c-ae71-b66a56b8ef5f"
    message: str
    model: str | None = None
    temperature: float | None = None


@router.post("/chat/stream")
async def chat_stream(
    req: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
):
    chat_stream_generator = await chat_service.chat_stream(
        topic_id=req.topic_id or "",
        message=req.message,
        model=req.model,
        temperature=req.temperature,
    )

    return StreamingResponse(
        content=chat_stream_generator,
        media_type="text/plain",
    )


@router.get("/chat/getTitle", response_class=EventSourceResponse)
async def get_title(
    title_queue: asyncio.Queue[str] = Depends(get_title_queue),
):
    yield ServerSentEvent(
        event="title.updated",
        data=json.dumps({"title": "Welcome to Alfred"}),
    )

    while True:
        title = await title_queue.get()
        yield ServerSentEvent(
            event="title.updated",
            data=json.dumps({"title": title}),
        )
