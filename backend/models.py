from typing import List
from pydantic import BaseModel, HttpUrl


class RunningServer(BaseModel):
    cmd: str
    description: str
    model: str
    name: str
    proxy: HttpUrl
    state: str
    ttl: int


class RunningResponse(BaseModel):
    running: List[RunningServer]


class ModelInfo(BaseModel):
    created: int
    id: str
    object: str
    owned_by: str


class ModelListResponse(BaseModel):
    data: List[ModelInfo]
    object: str
