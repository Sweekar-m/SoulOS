from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock

from backend.app.conversations.models import Conversation, ConversationMessage


class ConversationService:
    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._lock = RLock()

    def get(self, session_id: str) -> Conversation:
        with self._lock:
            return self._conversations.setdefault(session_id, Conversation(session_id=session_id))

    def append(self, session_id: str, role: str, content: str) -> ConversationMessage:
        message = ConversationMessage(
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            self._conversations.setdefault(session_id, Conversation(session_id=session_id)).messages.append(message)
        return message

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._conversations.pop(session_id, None)


conversation_service = ConversationService()
