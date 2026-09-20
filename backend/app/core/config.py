from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    version: str = os.getenv("SOULOS_VERSION", "0.1.0")
    api_base_url: str = os.getenv(
        "SOULOS_API_BASE_URL", "http://127.0.0.1:8000"
    )
    nim_base_url: str = os.getenv(
        "NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1"
    )
    nim_api_key: str = os.getenv("NVIDIA_NIM_API_KEY", "")
    nim_model: str = os.getenv("NVIDIA_NIM_MODEL", "")


settings = Settings()
