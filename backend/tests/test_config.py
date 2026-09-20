from backend.app.core.config import settings


def test_settings_have_safe_defaults() -> None:
    assert settings.version
    assert settings.api_base_url.startswith("http")
    assert settings.nim_base_url.startswith("http")
