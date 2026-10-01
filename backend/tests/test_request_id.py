from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_request_id_is_preserved() -> None:
    request_id = "soulos-test-request"
    response = client.get("/api/v1/health", headers={"X-Request-ID": request_id})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == request_id


def test_request_id_is_generated() -> None:
    response = client.get("/api/v1/health")
    assert len(response.headers["x-request-id"]) > 10
