from fastapi.testclient import TestClient

from backend.app.main import app


def test_generate_requires_text_input() -> None:
    response = TestClient(app).post("/api/v1/generate", json={})
    assert response.status_code == 422
