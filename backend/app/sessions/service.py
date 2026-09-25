from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4


class SessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, object]] = {}
        self._lock = RLock()

    def create(self) -> dict[str, object]:
        session_id = uuid4().hex
        session = {"session_id": session_id, "created_at": datetime.now(timezone.utc).isoformat()}
        with self._lock:
            self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> dict[str, object] | None:
        with self._lock:
            return self._sessions.get(session_id)

    def ensure(self, session_id: str | None) -> dict[str, object]:
        if session_id:
            existing = self.get(session_id)
            if existing:
                return existing
        return self.create()


session_service = SessionService()
