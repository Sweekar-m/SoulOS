from fastapi.testclient import TestClient

from backend.app.main import app


def test_models_endpoint_returns_safe_metadata() -> None:
    response = TestClient(app).get("/api/v1/models")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["models"], list)
    assert "api_key" not in response.text
    assert "Bearer " not in response.text


def test_models_health_endpoint_returns_documented_shape() -> None:
    response = TestClient(app).get("/api/v1/models/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "nvidia_nim"
    assert payload["status"] in {"ok", "unconfigured", "error"}
