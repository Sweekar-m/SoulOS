from __future__ import annotations

import re

_SECRET_KEYS = {"api_key", "token", "password", "secret", "authorization"}


def redact_mapping(values: dict[str, object]) -> dict[str, object]:
    """Return safe diagnostic data without exposing credential-like values."""
    result: dict[str, object] = {}
    for key, value in values.items():
        normalized = re.sub(r"[^a-z0-9]", "_", key.lower()).strip("_")
        result[key] = "[REDACTED]" if any(secret in normalized for secret in _SECRET_KEYS) else value
    return result
