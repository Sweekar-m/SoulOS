import httpx

from backend.app.core.config import Settings, settings
from backend.app.llm.models import ChatMessage, ModelHealth, NimResponse


class NimConfigurationError(ValueError):
    """Raised when NVIDIA NIM credentials or model configuration is missing."""


class NimProviderError(RuntimeError):
    """Raised when NVIDIA NIM cannot provide a valid response."""


class NimClient:
    def __init__(
        self,
        client: httpx.Client | None = None,
        runtime_settings: Settings = settings,
    ) -> None:
        self.settings = runtime_settings
        self._client = client or httpx.Client(
            base_url=self.settings.nim_base_url.rstrip("/") + "/",
            timeout=self.settings.nim_timeout_seconds,
        )

    def _require_configuration(self, model: str | None = None) -> str:
        api_key = self.settings.nim_api_key.strip()
        selected_model = (model or self.settings.nim_model).strip()
        if not api_key or not selected_model:
            raise NimConfigurationError(
                "NVIDIA NIM credentials are not configured"
            )
        return selected_model

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.settings.nim_api_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> NimResponse:
        selected_model = self._require_configuration(model)
        payload = {
            "model": selected_model,
            "messages": [message.model_dump() for message in messages],
            "temperature": (
                self.settings.nim_temperature
                if temperature is None
                else temperature
            ),
            "max_tokens": (
                self.settings.nim_max_tokens
                if max_tokens is None
                else max_tokens
            ),
        }

        try:
            response = self._client.post(
                "chat/completions",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as exc:
            raise NimProviderError(
                "NVIDIA NIM request timed out"
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise NimProviderError(
                f"NVIDIA NIM returned HTTP {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise NimProviderError(
                "NVIDIA NIM could not be reached"
            ) from exc
        except ValueError as exc:
            raise NimProviderError(
                "NVIDIA NIM returned invalid JSON"
            ) from exc

        try:
            choice = data["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason")
            usage = data.get("usage") or {}
            normalized_usage = {
                str(key): int(value)
                for key, value in usage.items()
                if isinstance(value, int)
            }
            if not isinstance(content, str) or not content.strip():
                raise ValueError
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise NimProviderError(
                "NVIDIA NIM returned a malformed chat response"
            ) from exc

        return NimResponse(
            content=content,
            model=selected_model,
            finish_reason=finish_reason,
            usage=normalized_usage,
        )

    def health(self) -> ModelHealth:
        api_key = self.settings.nim_api_key.strip()
        selected_model = self.settings.nim_model.strip() or None
        if not api_key or not selected_model:
            return ModelHealth(
                status="unconfigured",
                model=selected_model,
                detail="NVIDIA NIM credentials or model are not configured",
            )

        try:
            response = self._client.get("models", headers=self._headers())
            response.raise_for_status()
        except httpx.TimeoutException:
            return ModelHealth(
                status="error",
                model=selected_model,
                detail="NVIDIA NIM health check timed out",
            )
        except httpx.HTTPStatusError as exc:
            return ModelHealth(
                status="error",
                model=selected_model,
                detail=f"NVIDIA NIM health check returned HTTP {exc.response.status_code}",
            )
        except httpx.RequestError:
            return ModelHealth(
                status="error",
                model=selected_model,
                detail="NVIDIA NIM health check could not reach the provider",
            )
        return ModelHealth(status="ok", model=selected_model)
