from fastapi.testclient import TestClient

from backend.app.main import app


def test_diagnostics_is_secret_free() -> None:
    response = TestClient(app).get("/api/v1/diagnostics")
    assert response.status_code == 200
    body = response.json()
    serialized = str(body).lower()
    assert "api_key" not in serialized
    assert "secret" not in serialized
