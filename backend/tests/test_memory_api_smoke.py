from fastapi.testclient import TestClient

from backend.app.main import app


def test_memory_store_and_retrieve_are_session_scoped() -> None:
    client = TestClient(app)
    session_id = client.post("/api/v1/sessions").json()["session_id"]
    stored = client.post("/api/v1/memory/store", json={"session_id": session_id, "key": "theme", "value": "dark"})
    assert stored.status_code == 200
    retrieved = client.post("/api/v1/memory/retrieve", json={"session_id": session_id, "query": "theme"})
    assert retrieved.status_code == 200
    assert retrieved.json()["records"][0]["value"] == "dark"
