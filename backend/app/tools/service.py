from __future__ import annotations

from typing import Any

from backend.app.tools.audit import audit_log
from backend.app.tools.base import ToolResult
from backend.app.tools.catalog import builtin_tools
from backend.app.tools.events import tool_event
from backend.app.tools.registry import ToolRegistry


registry = ToolRegistry(builtin_tools())


def execute_registered(name: str, arguments: dict[str, Any], confirmed: bool = False) -> ToolResult:
    tool = registry.get(name)
    if tool.destructive and not confirmed:
        return ToolResult(success=False, error="explicit confirmation required")
    validated = tool.validate(arguments)
    started = tool_event("tool.started", tool.name)
    audit_log.record(started)
    result = tool.execute(validated)
    completed = tool_event("tool.completed", tool.name, success=result.success)
    audit_log.record(completed)
    result.events.extend([started, completed])
    return result
