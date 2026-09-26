from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.tools.presentation import PresentationTool

router = APIRouter(prefix="/generate", tags=["generation"])
_tool = PresentationTool()


class PresentationRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    slides: int = Field(default=8, ge=3, le=30)


@router.post("/presentation")
def generate_presentation(request: PresentationRequest) -> dict:
    args = _tool.validate(request.model_dump())
    result = _tool.execute(args)
    return {"success": result.success, "result": result.model_dump()}
