from asyncio import Queue
from services.models import LLMMessage
from services.llm import LLMService
from models.message import Message
from repositories.message_repository import MessageRepository


def build_messages(
    history: list[Message], max_messages: int = 10000
) -> list[LLMMessage]:

    recent_history = history[-max_messages:]
    return [LLMMessage(role=m.role, content=m.content) for m in recent_history]


class ChatService:
    def __init__(
        self,
        message_repository: MessageRepository,
        llm_service: LLMService,
        title_queue: Queue[str],
    ):
        self.message_repository = message_repository
        self.llm_service = llm_service
        self.title_queue = title_queue

    async def chat_stream(
        self, topic_id: str, message: str, model: str | None, temperature: float | None
    ):
        await self.message_repository.add(topic_id or "", "user", message)
        history = await self.message_repository.list_all()

        messages = build_messages(history)

        async def generate_and_save():
            full_response = []
            async for chunk in self.llm_service.stream_llm(
                model=model,
                temperature=temperature,
                messages=messages,
                title_queue=self.title_queue,
            ):
                full_response.append(chunk)
                yield chunk
            # Save after stream completes
            await self.message_repository.add(
                topic_id or "", "assistant", "".join(full_response)
            )

        return generate_and_save()
