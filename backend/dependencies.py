import os
import asyncio
from services.llm import LLMService
from services.chat import ChatService
from repositories.topic_repository import TopicRepository
from fastapi import Request, Depends
from db.unit_of_work import UnitOfWork
from repositories.message_repository import MessageRepository

title_queue: asyncio.Queue[str] = asyncio.Queue()


def get_uow(request: Request) -> UnitOfWork:
    return UnitOfWork(request.app.state.db_pool)


async def get_db(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        yield conn


def get_message_repo(conn=Depends(get_db)) -> MessageRepository:
    return MessageRepository(conn)


def get_topic_repo(conn=Depends(get_db)) -> TopicRepository:
    return TopicRepository(conn)


def get_llm_service():
    return LLMService(base_url=os.environ["BASE_URL"])


def get_title_queue() -> asyncio.Queue[str]:
    return title_queue


def get_chat_service(
    message_repository: MessageRepository = Depends(get_message_repo),
    llm_service: LLMService = Depends(get_llm_service),
    title_queue: asyncio.Queue[str] = Depends(get_title_queue),
) -> ChatService:
    return ChatService(
        message_repository=message_repository,
        llm_service=llm_service,
        title_queue=title_queue,
    )
