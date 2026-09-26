from __future__ import annotations

from collections import deque
from typing import Any


class ToolAuditLog:
    """Small bounded in-process audit buffer for desktop tool activity."""

    def __init__(self, max_entries: int = 200) -> None:
        self._entries: deque[dict[str, Any]] = deque(maxlen=max_entries)

    def record(self, event: dict[str, Any]) -> None:
        self._entries.append(dict(event))

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        return list(self._entries)[-max(1, min(limit, len(self._entries))):]


audit_log = ToolAuditLog()
