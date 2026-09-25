from backend.app.core.security import redact_mapping


def test_redacts_credential_like_keys() -> None:
    safe = redact_mapping({"NVIDIA_NIM_API_KEY": "secret", "region": "local"})

    assert safe["NVIDIA_NIM_API_KEY"] == "[REDACTED]"
    assert safe["region"] == "local"
