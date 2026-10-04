from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.diagnostics import public_snapshot

router = APIRouter(prefix="/diagnostics", tags=["system"])


class DiagnosticsResponse(BaseModel):
    service: str
    version: str
    api: str
    environment: str
    cors_origins: list[str]
    configured_models: int
    ready_services: int
    total_services: int


@router.get("", response_model=DiagnosticsResponse)
def diagnostics() -> DiagnosticsResponse:
    """Return safe runtime diagnostics without exposing credentials."""
    return DiagnosticsResponse(**public_snapshot())
