from dataclasses import dataclass

from backend.app.core.config import settings


@dataclass(frozen=True)
class ServiceHealth:
    name: str
    status: str
    detail: str


def backend_health() -> ServiceHealth:
    return ServiceHealth(
        name="soulos-backend",
        status="ok",
        detail=f"version={settings.version}",
    )


def readiness() -> list[ServiceHealth]:
    return [backend_health()]
