from fastapi.testclient import TestClient

from backend.app.main import app


def test_chat_rejects_empty_message() -> None:
    response = TestClient(app).post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_rejects_oversized_message() -> None:
    response = TestClient(app).post("/api/v1/chat", json={"message": "x" * 12001})
    assert response.status_code == 422
