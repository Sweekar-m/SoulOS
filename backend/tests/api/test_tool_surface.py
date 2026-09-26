from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_tools_endpoint_exposes_explicit_registry():
    response = client.get("/api/v1/tools")
    assert response.status_code == 200
    names = {item["name"] for item in response.json()["tools"]}
    assert "system.open_app" in names
    assert "web.search" in names


def test_unknown_tool_is_rejected():
    response = client.post("/api/v1/tools/execute", json={"name": "missing", "arguments": {}})
    assert response.status_code == 404
