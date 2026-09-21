from __future__ import annotations

from collections.abc import Iterable

from .base import Tool


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    def list(self) -> list[Tool]:
        return [self._tools[name] for name in sorted(self._tools)]

    def metadata(self) -> list[dict]:
        return [tool.metadata() for tool in self.list()]
