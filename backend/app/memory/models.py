from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


class MemoryRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=128)
    key: str = Field(min_length=1, max_length=128)
    value: str = Field(min_length=1, max_length=8000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=128)
    query: str = Field(min_length=1, max_length=512)
