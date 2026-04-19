from fastapi import Request, Depends
from db.unit_of_work import UnitOfWork
from repositories.message_repository import MessageRepository


def get_uow(request: Request) -> UnitOfWork:
    return UnitOfWork(request.app.db_pool.pool)


async def get_db(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        yield conn


def get_message_repo(conn=Depends(get_db)) -> MessageRepository:
    return MessageRepository(conn)
