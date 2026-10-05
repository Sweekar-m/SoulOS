from fastapi.testclient import TestClient

from backend.app.main import app


def test_tools_endpoint_returns_registered_metadata() -> None:
    response = TestClient(app).get("/api/v1/tools")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    for tool in body:
        assert "name" in tool
        assert "description" in tool
