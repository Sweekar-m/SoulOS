from backend.app.tools.service import execute_registered, registry


def test_registered_tools_are_explicit():
    assert registry.get("system.open_app").name == "system.open_app"


def test_invalid_tool_arguments_fail_before_execution():
    result = execute_registered("web.search", {"query": "x" * 501})
    assert result.success is False or result.error is not None
