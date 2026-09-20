from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class NimResponse(BaseModel):
    content: str = Field(min_length=1)
    model: str
    provider: str = "nvidia_nim"
    finish_reason: str | None = None
    usage: dict[str, int] = Field(default_factory=dict)


class ModelRoute(BaseModel):
    provider: str
    model: str
    reason: str
    requires_generation: bool = True


class ModelHealth(BaseModel):
    status: Literal["ok", "unconfigured", "error"]
    provider: str = "nvidia_nim"
    model: str | None = None
    detail: str | None = None
