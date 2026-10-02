from fastapi.testclient import TestClient

from backend.app.main import app


def test_request_id_is_returned_and_client_value_is_preserved() -> None:
    client = TestClient(app)
    generated = client.get("/api/v1/health")
    assert generated.headers.get("x-request-id")

    supplied = client.get("/api/v1/health", headers={"X-Request-ID": "test-request-123"})
    assert supplied.headers["x-request-id"] == "test-request-123"
