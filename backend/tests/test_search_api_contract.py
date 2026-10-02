from fastapi.testclient import TestClient

from backend.app.main import app


def test_search_requires_a_query() -> None:
    response = TestClient(app).post("/api/v1/search", json={})
    assert response.status_code == 422
