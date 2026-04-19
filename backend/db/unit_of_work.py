import asyncpg
from repositories.message_repository import MessageRepository


class UnitOfWork:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def __aenter__(self) -> "UnitOfWork":
        self._conn = await self._pool.acquire()
        self._tx = self._conn.transaction()
        await self._tx.start()

        self.messages = MessageRepository(self._conn)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._tx.rollback()
        else:
            await self._tx.commit()
        await self._pool.release(self._conn)
