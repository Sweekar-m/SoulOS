from fastapi.testclient import TestClient

from backend.app.main import app


def test_health_endpoint_returns_service_contract() -> None:
    response = TestClient(app).get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"ok", "degraded"}
    assert payload["service"]
    assert payload["version"]
