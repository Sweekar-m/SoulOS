from fastapi import APIRouter, HTTPException, status

from backend.app.tools.audit import audit_log
from backend.app.tools.schemas import ToolExecutionRequest, ToolExecutionResponse
from backend.app.tools.service import execute_registered, registry

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
def list_tools() -> dict:
    return {"tools": registry.metadata()}


@router.get("/activity")
def tool_activity(limit: int = 25) -> dict:
    return {"events": audit_log.recent(limit)}


@router.post("/execute", response_model=ToolExecutionResponse)
def execute_tool(request: ToolExecutionRequest) -> ToolExecutionResponse:
    try:
        result = execute_registered(request.name, request.arguments, request.confirmed)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    if not result.success and result.error == "explicit confirmation required":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result.error)

    return ToolExecutionResponse(name=request.name, result=result.model_dump())
