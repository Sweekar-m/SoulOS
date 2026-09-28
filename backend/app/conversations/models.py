from __future__ import annotations

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1, max_length=12000)
    created_at: str


class Conversation(BaseModel):
    session_id: str
    messages: list[ConversationMessage] = Field(default_factory=list)
