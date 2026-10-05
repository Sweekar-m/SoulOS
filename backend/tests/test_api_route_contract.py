from backend.app.main import app


def test_documented_api_routes_are_registered() -> None:
    routes = {route.path for route in app.routes}
    expected = {
        "/api/v1/health",
        "/api/v1/ready",
        "/api/v1/meta",
        "/api/v1/diagnostics",
        "/api/v1/models",
        "/api/v1/models/health",
        "/api/v1/intents",
        "/api/v1/tools",
        "/api/v1/tools/execute",
        "/api/v1/memory/store",
        "/api/v1/memory/retrieve",
        "/api/v1/sessions",
        "/api/v1/sessions/{session_id}",
        "/api/v1/conversations/{session_id}",
        "/api/v1/conversations/{session_id}/messages",
        "/api/v1/chat",
        "/api/v1/search",
        "/api/v1/generate",
    }
    assert expected <= routes
