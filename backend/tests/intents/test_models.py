import pytest
from pydantic import ValidationError

from backend.app.intents.models import IntentRequest


def test_blank_intent_request_is_rejected() -> None:
    with pytest.raises(ValidationError):
        IntentRequest(text="   ")


def test_intent_request_normalizes_whitespace() -> None:
    request = IntentRequest(text="  open   chrome ")
    assert request.text == "open chrome"
