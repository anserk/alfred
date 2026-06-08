import uuid
import asyncpg
from queries import message_queries as q
from models.message import Message


class MessageRepository:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def list_all(self) -> list[Message]:
        """
        Return all messages
        """
        rows = await self._conn.fetch(q.LIST_ALL, 1000)
        return [Message.model_validate(dict(row)) for row in rows]

    async def add(self, topic_id: str, role: str, content: str) -> None:
        """
        Save a new message into a conversation.
        """
        await self._conn.execute(q.INSERT_NEW, uuid.UUID(topic_id), role, content)
        return
