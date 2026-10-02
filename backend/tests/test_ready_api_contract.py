from fastapi.testclient import TestClient

from backend.app.main import app


def test_ready_reports_service_breakdown() -> None:
    response = TestClient(app).get("/api/v1/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"ready", "degraded"}
    assert isinstance(body["services"], list)
    assert all({"name", "status"}.issubset(item) for item in body["services"])
