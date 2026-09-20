from dataclasses import dataclass
import json
import os


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _specialist_models() -> dict[str, str]:
    raw = os.getenv("NVIDIA_NIM_SPECIALIST_MODELS", "").strip()
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(value, dict):
        return {}
    return {
        str(intent): str(model)
        for intent, model in value.items()
        if str(intent).strip() and str(model).strip()
    }


@dataclass(frozen=True)
class Settings:
    version: str = "0.1.0"
    api_base_url: str = "http://127.0.0.1:8000"
    nim_base_url: str = "https://integrate.api.nvidia.com/v1"
    nim_api_key: str = ""
    nim_model: str = ""
    nim_timeout_seconds: float = 30.0
    nim_temperature: float = 0.2
    nim_max_tokens: int = 1024
    nim_specialist_models: dict[str, str] = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            version=os.getenv("SOULOS_VERSION", "0.1.0"),
            api_base_url=os.getenv(
                "SOULOS_API_BASE_URL", "http://127.0.0.1:8000"
            ),
            nim_base_url=os.getenv(
                "NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1"
            ),
            nim_api_key=os.getenv("NVIDIA_NIM_API_KEY", ""),
            nim_model=os.getenv("NVIDIA_NIM_MODEL", ""),
            nim_timeout_seconds=_float_env("NVIDIA_NIM_TIMEOUT_SECONDS", 30.0),
            nim_temperature=_float_env("NVIDIA_NIM_TEMPERATURE", 0.2),
            nim_max_tokens=_int_env("NVIDIA_NIM_MAX_TOKENS", 1024),
            nim_specialist_models=_specialist_models(),
        )


settings = Settings.from_env()
