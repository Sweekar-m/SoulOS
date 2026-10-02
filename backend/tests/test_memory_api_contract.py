from fastapi.testclient import TestClient

from backend.app.main import app


def test_memory_store_and_retrieve_round_trip() -> None:
    client = TestClient(app)
    session_id = client.post("/api/v1/sessions").json()["session_id"]
    stored = client.post("/api/v1/memory/store", json={
        "session_id": session_id,
        "key": "preference",
        "value": "concise",
    })
    assert stored.status_code == 200
    retrieved = client.post("/api/v1/memory/retrieve", json={
        "session_id": session_id,
        "query": "preference",
    })
    assert retrieved.status_code == 200
    assert any(item["key"] == "preference" for item in retrieved.json()["records"])
