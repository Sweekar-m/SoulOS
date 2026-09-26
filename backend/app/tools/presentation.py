from __future__ import annotations

from pydantic import BaseModel, Field

from backend.app.tools.base import Tool, ToolResult


class PresentationArguments(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    slides: int = Field(default=8, ge=3, le=30)


class PresentationTool(Tool):
    name = "presentation.generate"
    description = "Validate a presentation-generation request before invoking a generator."
    arguments_model = PresentationArguments

    def execute(self, arguments: PresentationArguments) -> ToolResult:
        return ToolResult(
            success=False,
            error="presentation generator is not configured",
            output={"topic": arguments.topic, "slides": arguments.slides},
        )


PRESENTATION_TOOLS: tuple[Tool, ...] = (PresentationTool(),)
