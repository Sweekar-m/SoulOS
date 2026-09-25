from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.memory.models import MemoryRecord
from backend.app.memory.service import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])


class StoreMemoryRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    key: str = Field(min_length=1, max_length=128)
    value: str = Field(min_length=1, max_length=8000)


class RetrieveMemoryRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    query: str = Field(min_length=1, max_length=512)


class MemoryResponse(BaseModel):
    records: list[MemoryRecord]


@router.post("/store", response_model=MemoryRecord)
def store_memory(request: StoreMemoryRequest) -> MemoryRecord:
    return memory_service.store(request.session_id, request.key, request.value)


@router.post("/retrieve", response_model=MemoryResponse)
def retrieve_memory(request: RetrieveMemoryRequest) -> MemoryResponse:
    return MemoryResponse(records=memory_service.retrieve(request.session_id, request.query))
