import logging
from fastapi import FastAPI
import asyncpg
from contextlib import asynccontextmanager
import os
from routers import topics, chat

DATABASE_URL = os.environ["DATABASE_URL"]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
app.include_router(topics.router)
app.include_router(chat.router)
