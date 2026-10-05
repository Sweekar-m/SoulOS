from fastapi.testclient import TestClient

from backend.app.main import app


def test_api_response_preserves_client_request_id() -> None:
    response = TestClient(app).get("/api/v1/meta", headers={"X-Request-ID": "test-request-123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"
