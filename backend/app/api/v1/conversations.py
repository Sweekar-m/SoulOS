from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.conversations.models import Conversation, ConversationMessage
from backend.app.conversations.service import conversation_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


class AppendMessageRequest(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1, max_length=12000)


@router.get("/{session_id}", response_model=Conversation)
def get_conversation(session_id: str) -> Conversation:
    return conversation_service.get(session_id)


@router.post("/{session_id}/messages", response_model=ConversationMessage)
def append_message(session_id: str, request: AppendMessageRequest) -> ConversationMessage:
    return conversation_service.append(session_id, request.role, request.content)


@router.delete("/{session_id}", status_code=204)
def clear_conversation(session_id: str) -> None:
    conversation_service.clear(session_id)
