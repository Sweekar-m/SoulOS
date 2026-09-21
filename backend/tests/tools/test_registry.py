from pydantic import BaseModel
import pytest

from backend.app.tools.base import Tool, ToolResult
from backend.app.tools.registry import ToolRegistry


class EchoArguments(BaseModel):
    value: str


class EchoTool(Tool):
    name = "test.echo"
    description = "Echo a value for registry tests."
    arguments_model = EchoArguments

    def execute(self, arguments: EchoArguments) -> ToolResult:
        return ToolResult(success=True, output=arguments.value)


def test_registry_lists_tools_deterministically() -> None:
    registry = ToolRegistry([EchoTool()])
    assert [item["name"] for item in registry.metadata()] == ["test.echo"]


def test_registry_rejects_duplicate_names() -> None:
    registry = ToolRegistry([EchoTool()])
    with pytest.raises(ValueError, match="already registered"):
        registry.register(EchoTool())


def test_registry_rejects_unknown_tool() -> None:
    registry = ToolRegistry([EchoTool()])
    with pytest.raises(KeyError, match="unknown tool"):
        registry.get("missing")


def test_tool_contract_validates_arguments() -> None:
    tool = EchoTool()
    assert tool.validate({"value": "ok"}).value == "ok"
    with pytest.raises(ValueError):
        tool.validate({"value": 123})
