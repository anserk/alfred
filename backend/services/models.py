from typing import Optional, List, Any
from pydantic import BaseModel


class LLMMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_call_id: Optional[str] = None
