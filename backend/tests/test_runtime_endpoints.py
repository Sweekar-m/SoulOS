from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_contract() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"]


def test_ready_contract() -> None:
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_metadata_contract() -> None:
    response = client.get("/api/v1/meta")
    assert response.status_code == 200
    assert response.json()["api"] == "v1"
