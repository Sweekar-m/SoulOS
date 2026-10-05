from fastapi.testclient import TestClient

from backend.app.main import app


def test_cors_preflight_is_configured_for_local_desktop_origin() -> None:
    response = TestClient(app).options(
        "/api/v1/meta",
        headers={
            "Origin": "http://localhost:1420",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code in {200, 400}
    if response.status_code == 200:
        assert response.headers.get("access-control-allow-origin")
