from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.tools.search import WebSearchArguments, WebSearchTool

router = APIRouter(prefix="/search", tags=["search"])
_tool = WebSearchTool()


class SearchResponse(BaseModel):
    success: bool
    query: str
    limit: int
    error: str | None = None


@router.get("", response_model=SearchResponse)
def search(query: str = Field(min_length=2, max_length=500), limit: int = 5) -> SearchResponse:
    args = _tool.validate({"query": query, "limit": limit})
    result = _tool.execute(args)
    return SearchResponse(success=result.success, query=args.query, limit=args.limit, error=result.error)
