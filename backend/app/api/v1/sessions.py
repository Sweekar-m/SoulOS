from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.sessions.service import session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionResponse(BaseModel):
    session_id: str = Field(min_length=1)
    created_at: str


@router.post("", response_model=SessionResponse)
def create_session() -> SessionResponse:
    return SessionResponse(**session_service.create())


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str) -> SessionResponse:
    session = session_service.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    return SessionResponse(**session)
