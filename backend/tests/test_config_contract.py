from backend.app.core.config import Settings


def test_settings_parse_cors_and_nim_specialists(monkeypatch) -> None:
    monkeypatch.setenv("SOULOS_CORS_ORIGINS", "http://one.test, http://two.test")
    monkeypatch.setenv("NVIDIA_NIM_SPECIALIST_MODELS", '{"coding":"model-a","chat":"model-b"}')
    loaded = Settings.from_env()
    assert loaded.cors_origins == ("http://one.test", "http://two.test")
    assert loaded.nim_specialist_models == {"coding": "model-a", "chat": "model-b"}
