from fastapi.testclient import TestClient

from backend.app.main import app


def test_intent_endpoint_returns_routeable_classification() -> None:
    response = TestClient(app).post("/api/v1/intents", json={"message": "hello SoulOS"})
    assert response.status_code == 200
    body = response.json()
    assert body["intent"]
    assert 0 <= body["confidence"] <= 1
