from fastapi.testclient import TestClient

from backend.app.main import app


def test_intent_endpoint_classifies_request() -> None:
    response = TestClient(app).post(
        "/api/v1/intents",
        json={"text": "open chrome"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "system.open_app"
    assert payload["entities"]["application"] == "chrome"


def test_intent_endpoint_rejects_blank_text() -> None:
    response = TestClient(app).post(
        "/api/v1/intents",
        json={"text": "   "},
    )
    assert response.status_code == 422
