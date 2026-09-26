from __future__ import annotations

from pydantic import BaseModel, Field

from backend.app.tools.base import Tool, ToolResult


class WebSearchArguments(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    limit: int = Field(default=5, ge=1, le=10)


class WebSearchTool(Tool):
    name = "web.search"
    description = "Validate a web-search request for a future search provider adapter."
    arguments_model = WebSearchArguments

    def execute(self, arguments: WebSearchArguments) -> ToolResult:
        return ToolResult(
            success=False,
            error="no web search provider is configured",
            output={"query": arguments.query, "limit": arguments.limit},
        )


WEB_TOOLS: tuple[Tool, ...] = (WebSearchTool(),)
