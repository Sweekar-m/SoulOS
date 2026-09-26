from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def tool_event(event_type: str, tool: str, **payload: Any) -> dict[str, Any]:
    """Create a stable observable event for desktop activity rendering."""
    return {
        "type": event_type,
        "tool": tool,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
