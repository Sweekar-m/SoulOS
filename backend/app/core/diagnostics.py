from dataclasses import asdict, dataclass

from backend.app.core.config import settings
from backend.app.core.health import readiness


@dataclass(frozen=True)
class DiagnosticSnapshot:
    service: str
    version: str
    api: str
    environment: str
    cors_origins: tuple[str, ...]
    configured_models: int
    ready_services: int
    total_services: int


def snapshot() -> DiagnosticSnapshot:
    services = readiness()
    configured_models = int(bool(settings.nim_model)) + sum(
        1 for model in settings.nim_specialist_models.values() if model
    )
    return DiagnosticSnapshot(
        service="SoulOS Backend",
        version=settings.version,
        api="v1",
        environment=settings.environment,
        cors_origins=tuple(settings.cors_origins),
        configured_models=configured_models,
        ready_services=sum(item.status == "ok" for item in services),
        total_services=len(services),
    )


def public_snapshot() -> dict:
    data = asdict(snapshot())
    data["cors_origins"] = list(data["cors_origins"])
    return data
