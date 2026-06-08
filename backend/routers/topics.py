from pydantic import BaseModel
from dependencies import get_topic_repo
from repositories.topic_repository import TopicRepository
from fastapi import APIRouter, Depends
from uuid import UUID

router = APIRouter()


class TopicDto(BaseModel):
    id: UUID
    title: str
    summary: str | None = None


@router.get("/topics")
async def get_topics(
    repo: TopicRepository = Depends(get_topic_repo),
) -> list[TopicDto]:
    return [
        TopicDto(id=t.id, title=t.title, summary=t.summary)
        for t in await repo.list_all()
    ]
