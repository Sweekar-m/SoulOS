from fastapi import APIRouter, HTTPException, status

from backend.app.tools.runtime import registry
from backend.app.tools.schemas import ToolExecutionRequest, ToolExecutionResponse

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
def list_tools() -> dict:
    return {"tools": registry.metadata()}


@router.post("/execute", response_model=ToolExecutionResponse)
def execute_tool(request: ToolExecutionRequest) -> ToolExecutionResponse:
    try:
        tool = registry.get(request.name)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if tool.destructive and not request.confirmed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="tool execution requires explicit confirmation",
        )

    try:
        arguments = tool.validate(request.arguments)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    result = tool.execute(arguments)
    return ToolExecutionResponse(name=tool.name, result=result.model_dump())
