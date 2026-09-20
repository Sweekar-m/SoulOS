import httpx
import pytest

from backend.app.core.config import Settings
from backend.app.llm.models import ChatMessage
from backend.app.llm.nim_client import (
    NimClient,
    NimConfigurationError,
    NimProviderError,
)


def _client(handler, **overrides) -> NimClient:
    runtime_settings = Settings(
        nim_base_url="https://nim.test/v1",
        nim_api_key="test-key",
        nim_model="test-model",
        nim_specialist_models={},
        **overrides,
    )
    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url=runtime_settings.nim_base_url.rstrip("/") + "/",
    )
    return NimClient(client=client, runtime_settings=runtime_settings)


def test_chat_normalizes_successful_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {"content": "Hello from NIM"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 3, "completion_tokens": 4},
            },
        )

    response = _client(handler).chat(
        [ChatMessage(role="user", content="hello")]
    )
    assert response.content == "Hello from NIM"
    assert response.model == "test-model"
    assert response.usage == {"prompt_tokens": 3, "completion_tokens": 4}


def test_chat_rejects_provider_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    with pytest.raises(NimProviderError, match="timed out"):
        _client(handler).chat([ChatMessage(role="user", content="hello")])


def test_chat_rejects_provider_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "unavailable"})

    with pytest.raises(NimProviderError, match="HTTP 503"):
        _client(handler).chat([ChatMessage(role="user", content="hello")])


def test_chat_rejects_malformed_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"choices": []})

    with pytest.raises(NimProviderError, match="malformed"):
        _client(handler).chat([ChatMessage(role="user", content="hello")])


def test_chat_requires_credentials_and_model() -> None:
    runtime_settings = Settings(
        nim_api_key="",
        nim_model="",
        nim_specialist_models={},
    )
    client = NimClient(runtime_settings=runtime_settings)

    with pytest.raises(NimConfigurationError):
        client.chat([ChatMessage(role="user", content="hello")])
