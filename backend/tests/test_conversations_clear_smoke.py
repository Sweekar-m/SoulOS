from fastapi.testclient import TestClient

from backend.app.main import app


def test_conversation_delete_clears_session_history() -> None:
    client = TestClient(app)
    session_id = client.post("/api/v1/sessions").json()["session_id"]
    client.post(
        f"/api/v1/conversations/{session_id}/messages",
        json={"role": "user", "content": "temporary"},
    )
    cleared = client.delete(f"/api/v1/conversations/{session_id}")
    assert cleared.status_code == 204
    history = client.get(f"/api/v1/conversations/{session_id}")
    assert history.status_code == 200
    assert history.json()["messages"] == []
