from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "souls-backend",
        "version": settings.version,
    }
