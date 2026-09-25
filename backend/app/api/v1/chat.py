from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.intents.service import IntentService
from backend.app.llm.models import ChatMessage
from backend.app.llm.nim_client import NimClient, NimConfigurationError, NimProviderError
from backend.app.llm.router import LlmRouter
from backend.app.memory.service import memory_service
from backend.app.sessions.service import session_service

router = APIRouter(prefix="/chat", tags=["chat"])
_intents = IntentService()
_llm_router = LlmRouter()
_nim = NimClient()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    session_id: str | None = Field(default=None, max_length=128)


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    route: dict
    response: str
    tool_events: list[dict] = Field(default_factory=list)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session = session_service.ensure(request.session_id)
    session_id = str(session["session_id"])
    intent = _intents.classify(request.message)
    route = _llm_router.route(intent, {"session_id": session_id})

    if intent.requires_confirmation:
        return ChatResponse(
            session_id=session_id,
            intent=intent.intent,
            confidence=intent.confidence,
            route=route.model_dump(),
            response="This action needs explicit confirmation before execution.",
        )

    if not route.requires_generation:
        raise HTTPException(status_code=409, detail="tool intent requires explicit tool execution")

    context_records = memory_service.retrieve(session_id, request.message, limit=5)
    context = "\n".join(f"{record.key}: {record.value}" for record in context_records)
    prompt = request.message if not context else f"Relevant memory:\n{context}\n\nUser: {request.message}"

    try:
        result = _nim.chat([ChatMessage(role="user", content=prompt)], model=route.model or None)
    except (NimConfigurationError, NimProviderError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(
        session_id=session_id,
        intent=intent.intent,
        confidence=intent.confidence,
        route=route.model_dump(),
        response=result.content,
    )
