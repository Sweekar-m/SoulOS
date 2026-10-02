from fastapi.testclient import TestClient

from backend.app.main import app


def test_models_endpoint_never_exposes_nim_credentials() -> None:
    payload = TestClient(app).get("/api/v1/models").json()
    assert "models" in payload
    assert "api_key" not in payload
    assert "nim_api_key" not in str(payload).lower()
