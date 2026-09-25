from __future__ import annotations

from collections import defaultdict
from threading import RLock

from .models import MemoryRecord


class MemoryService:
    """Small process-local memory store; external persistence can be added later."""

    def __init__(self) -> None:
        self._records: dict[str, list[MemoryRecord]] = defaultdict(list)
        self._lock = RLock()

    def store(self, session_id: str, key: str, value: str) -> MemoryRecord:
        record = MemoryRecord(session_id=session_id, key=key, value=value)
        with self._lock:
            records = self._records[session_id]
            records[:] = [item for item in records if item.key != key]
            records.append(record)
        return record

    def retrieve(self, session_id: str, query: str, limit: int = 10) -> list[MemoryRecord]:
        needle = query.strip().lower()
        with self._lock:
            records = list(self._records.get(session_id, ()))
        if not needle:
            return records[-limit:]
        matches = [r for r in records if needle in r.key.lower() or needle in r.value.lower()]
        return matches[-limit:]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._records.pop(session_id, None)


memory_service = MemoryService()
