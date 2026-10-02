from fastapi.testclient import TestClient

from backend.app.main import app


def test_conversation_message_is_persisted_for_session() -> None:
    client = TestClient(app)
    session_id = client.post("/api/v1/sessions").json()["session_id"]
    response = client.post(
        f"/api/v1/conversations/{session_id}/messages",
        json={"role": "user", "content": "remember this"},
    )
    assert response.status_code == 200
    history = client.get(f"/api/v1/conversations/{session_id}")
    assert history.status_code == 200
    assert history.json()["messages"][-1]["content"] == "remember this"
