from backend.app.api.v1.diagnostics import diagnostics


def test_diagnostics_returns_safe_runtime_shape() -> None:
    payload = diagnostics()

    assert payload["service"] == "SoulOS Backend"
    assert payload["api"] == "v1"
    assert isinstance(payload["cors_origins"], list)
    assert isinstance(payload["configured_models"], int)
    assert "nim_api_key" not in payload
    assert "api_key" not in payload
