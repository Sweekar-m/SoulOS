from fastapi.testclient import TestClient

from backend.app.main import app


def test_session_create_and_fetch_round_trip() -> None:
    client = TestClient(app)
    created = client.post("/api/v1/sessions")
    assert created.status_code == 200
    session_id = created.json()["session_id"]
    fetched = client.get(f"/api/v1/sessions/{session_id}")
    assert fetched.status_code == 200
    assert fetched.json()["session_id"] == session_id
