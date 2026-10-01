from fastapi import FastAPI

from backend.app.api.v1.router import router as api_router
from backend.app.core.config import settings
from backend.app.core.request_id import RequestIdMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="SoulOS Backend", version=settings.version)
    app.add_middleware(RequestIdMiddleware)
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
