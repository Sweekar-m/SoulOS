from backend.app.core.config import Settings


def test_settings_have_safe_defaults() -> None:
    settings = Settings.from_env()
    assert settings.version
    assert settings.api_base_url.startswith("http")
    assert settings.nim_base_url.startswith("http")
    assert "http://localhost:1420" in settings.cors_origins


def test_specialist_models_are_optional(monkeypatch) -> None:
    monkeypatch.delenv("NVIDIA_NIM_SPECIALIST_MODELS", raising=False)
    assert Settings.from_env().nim_specialist_models == {}
