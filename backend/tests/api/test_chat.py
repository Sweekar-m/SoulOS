from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.v1.chat import router


def test_chat_rejects_empty_message() -> None:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    client = TestClient(app)

    response = client.post("/api/v1/chat", json={"message": ""})

    assert response.status_code == 422
