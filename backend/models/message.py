from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Message(BaseModel):
    id: UUID
    topic_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
