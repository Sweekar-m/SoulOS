from backend.app.intents.entities import extract_entities
from backend.app.intents.service import IntentService


def test_application_entity_is_extracted() -> None:
    assert extract_entities("open chrome", "system.open_app") == {"application": "chrome"}


def test_low_confidence_commands_become_unknown() -> None:
    result = IntentService().classify("zzzz qqqq completely unrelated")
    assert result.intent == "unknown"
    assert result.requires_confirmation is False


def test_close_app_requires_confirmation_when_not_high_confidence() -> None:
    result = IntentService().classify("close some application")
    assert result.intent == "system.close_app"
    assert result.requires_confirmation is True
