from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_tools_endpoint_exposes_metadata_without_secrets() -> None:
    response = client.get("/api/v1/tools")
    assert response.status_code == 200
    payload = response.json()
    assert payload["tools"][0]["name"] == "system.open_app"
    assert "NVIDIA_API_KEY" not in response.text


def test_unknown_tool_is_rejected() -> None:
    response = client.post(
        "/api/v1/tools/execute",
        json={"name": "missing.tool", "arguments": {}},
    )
    assert response.status_code == 404


def test_invalid_tool_arguments_are_rejected() -> None:
    response = client.post(
        "/api/v1/tools/execute",
        json={"name": "system.open_app", "arguments": {"app": ""}},
    )
    assert response.status_code == 422
