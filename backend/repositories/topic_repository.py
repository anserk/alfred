import uuid
import asyncpg
from queries import topic_queries as q
from models.topic import Topic


class TopicRepository:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def list_all(self) -> list[Topic]:
        """
        Return all topics
        """
        rows = await self._conn.fetch(q.LIST_ALL)
        return [Topic.model_validate(dict(row)) for row in rows]

    async def add(self, title: str, summary: str) -> None:
        """
        Save a new message into a conversation.
        """
        await self._conn.execute(q.INSERT_NEW, uuid.uuid4(), title, summary)
        return

    async def update(self, id: uuid.UUID, summary: str):
        await self._conn.execute(q.UPDATE, id, summary)
        return
