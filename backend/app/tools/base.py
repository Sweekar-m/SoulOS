from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    output: Any = None
    error: str | None = None
    events: list[dict[str, Any]] = []


class Tool(ABC):
    name: str
    description: str
    destructive: bool = False
    arguments_model: type[BaseModel]

    @abstractmethod
    def execute(self, arguments: BaseModel) -> ToolResult:
        raise NotImplementedError

    def validate(self, arguments: dict[str, Any]) -> BaseModel:
        return self.arguments_model.model_validate(arguments)

    def metadata(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "destructive": self.destructive,
            "arguments": self.arguments_model.model_json_schema(),
        }
