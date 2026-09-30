from backend.app.tools.base import ToolResult


def test_tool_result_events_are_isolated():
    first = ToolResult(success=True)
    second = ToolResult(success=True)
    first.events.append({"type": "tool.completed"})
    assert second.events == []
