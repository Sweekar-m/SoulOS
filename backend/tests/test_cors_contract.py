from fastapi.testclient import TestClient

from backend.app.main import app


def test_configured_desktop_origin_is_allowed() -> None:
    response = TestClient(app).options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:1420",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:1420"
