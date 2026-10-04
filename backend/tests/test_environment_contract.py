from backend.app.core.config import Settings


def test_environment_defaults_to_development(monkeypatch) -> None:
    monkeypatch.delenv("SOULOS_ENVIRONMENT", raising=False)
    assert Settings.from_env().environment == "development"


def test_environment_can_be_configured(monkeypatch) -> None:
    monkeypatch.setenv("SOULOS_ENVIRONMENT", "test")
    assert Settings.from_env().environment == "test"
