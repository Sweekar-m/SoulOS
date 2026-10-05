from fastapi.testclient import TestClient

from backend.app.main import app


def test_conversation_message_round_trip() -> None:
    client = TestClient(app)
    session_id = client.post("/api/v1/sessions").json()["session_id"]
    appended = client.post(
        f"/api/v1/conversations/{session_id}/messages",
        json={"role": "user", "content": "hello"},
    )
    assert appended.status_code == 200
    history = client.get(f"/api/v1/conversations/{session_id}")
    assert history.status_code == 200
    assert history.json()["messages"][0]["content"] == "hello"
