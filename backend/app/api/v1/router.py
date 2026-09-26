from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.generate import router as generate_router
from backend.app.api.v1.intents import router as intents_router
from backend.app.api.v1.memory import router as memory_router
from backend.app.api.v1.search import router as search_router
from backend.app.api.v1.sessions import router as sessions_router
from backend.app.api.v1.system import router as system_router
from backend.app.api.v1.tools import router as tools_router
from backend.app.core.config import settings
from backend.app.llm.models import ModelHealth
from backend.app.llm.nim_client import NimClient

router = APIRouter()


class ModelInfo(BaseModel):
    provider: str
    model: str
    role: str
    intent: str | None = None


class ModelCatalog(BaseModel):
    models: list[ModelInfo]


_nim_client = NimClient()


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "souls-backend", "version": settings.version}


@router.get("/models", response_model=ModelCatalog, tags=["models"])
def list_models() -> ModelCatalog:
    models: list[ModelInfo] = []
    if settings.nim_model:
        models.append(ModelInfo(provider="nvidia_nim", model=settings.nim_model, role="primary"))
    for intent, model in sorted(settings.nim_specialist_models.items()):
        if model and model != settings.nim_model:
            models.append(ModelInfo(provider="nvidia_nim", model=model, role="specialist", intent=intent))
    return ModelCatalog(models=models)


@router.get("/models/health", response_model=ModelHealth, tags=["models"])
def models_health() -> ModelHealth:
    return _nim_client.health()


router.include_router(intents_router)
router.include_router(tools_router)
router.include_router(memory_router)
router.include_router(sessions_router)
router.include_router(chat_router)
router.include_router(search_router)
router.include_router(generate_router)
router.include_router(system_router)
