from fastapi import APIRouter

from backend.app.core.diagnostics import public_snapshot

router = APIRouter(prefix="/diagnostics", tags=["system"])


@router.get("")
def diagnostics() -> dict:
    """Return safe runtime diagnostics without exposing credentials."""
    return public_snapshot()
