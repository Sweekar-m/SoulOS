from backend.app.core.health import backend_health


def test_backend_health_includes_environment() -> None:
    value = backend_health()
    assert "version=" in value.detail
    assert "environment=" in value.detail
