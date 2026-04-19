from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ConversationOut(BaseModel):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
