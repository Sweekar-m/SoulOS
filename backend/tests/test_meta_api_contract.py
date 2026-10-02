from fastapi.testclient import TestClient

from backend.app.main import app


def test_meta_reports_versioned_api_contract() -> None:
    response = TestClient(app).get("/api/v1/meta")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "SoulOS Backend"
    assert body["api"] == "v1"
    assert body["version"]
