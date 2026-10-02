import httpx

from backend.app.core.config import Settings
from backend.app.llm.models import ChatMessage
from backend.app.llm.nim_client import NimClient


def test_nim_client_normalizes_chat_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/chat/completions")
        return httpx.Response(200, json={
            "choices": [{"message": {"content": "hello"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2},
        })

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://nim.test/v1/")
    settings = Settings(nim_api_key="secret", nim_model="test-model", nim_base_url="https://nim.test/v1")
    result = NimClient(client=client, runtime_settings=settings).chat([ChatMessage(role="user", content="hi")])
    assert result.content == "hello"
    assert result.model == "test-model"
    assert result.usage == {"prompt_tokens": 3, "completion_tokens": 2}
