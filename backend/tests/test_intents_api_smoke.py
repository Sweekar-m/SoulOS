from fastapi.testclient import TestClient

from backend.app.main import app


def test_intents_endpoint_accepts_natural_language_command() -> None:
    response = TestClient(app).post("/api/v1/intents", json={"text": "open the browser"})
    assert response.status_code == 200
    body = response.json()
    assert "intent" in body
