from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Topic(BaseModel):
    id: UUID
    title: str
    summary: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
