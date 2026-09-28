from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_conversation_api_round_trip() -> None:
    session_id = "api-conversation-test"
    response = client.post(
        f"/api/v1/conversations/{session_id}/messages",
        json={"role": "user", "content": "hello"},
    )
    assert response.status_code == 200

    response = client.get(f"/api/v1/conversations/{session_id}")
    assert response.status_code == 200
    assert response.json()["messages"][0]["content"] == "hello"

    response = client.delete(f"/api/v1/conversations/{session_id}")
    assert response.status_code == 204
