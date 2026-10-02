from fastapi.testclient import TestClient

from backend.app.main import app


def test_tools_endpoint_exposes_registered_metadata() -> None:
    response = TestClient(app).get("/api/v1/tools")
    assert response.status_code == 200
    assert isinstance(response.json()["tools"], list)


def test_unknown_tool_is_rejected() -> None:
    response = TestClient(app).post("/api/v1/tools/execute", json={"name": "missing-tool", "arguments": {}})
    assert response.status_code == 404
