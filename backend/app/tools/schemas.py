from __future__ import annotations

from pydantic import BaseModel, Field


class EmptyArguments(BaseModel):
    pass


class OpenAppArguments(BaseModel):
    app: str = Field(min_length=1, max_length=100)


class SearchArguments(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=10)


class PresentationArguments(BaseModel):
    topic: str = Field(min_length=1, max_length=200)
    slides: int = Field(default=8, ge=1, le=30)


class ToolExecutionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    arguments: dict = Field(default_factory=dict)
    confirmed: bool = False


class ToolExecutionResponse(BaseModel):
    name: str
    result: dict
