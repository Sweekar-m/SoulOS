from backend.app.core.config import Settings
from backend.app.intents.models import IntentResult
from backend.app.llm.router import LlmRouter


def _intent(name: str, confidence: float = 0.95) -> IntentResult:
    return IntentResult(
        intent=name,
        confidence=confidence,
        entities={},
        requires_confirmation=False,
    )


def test_system_actions_route_to_tools_without_generation() -> None:
    route = LlmRouter(Settings(
        nim_model="primary",
        nim_specialist_models={},
    )).route(_intent("system.open_app"))

    assert route.provider == "tool-runtime"
    assert route.requires_generation is False
    assert route.model == ""


def test_exact_specialist_model_override_wins() -> None:
    route = LlmRouter(Settings(
        nim_model="primary",
        nim_specialist_models={"knowledge.search": "researcher"},
    )).route(_intent("knowledge.search"))

    assert route.provider == "nvidia_nim"
    assert route.model == "researcher"


def test_family_specialist_override_is_supported() -> None:
    route = LlmRouter(Settings(
        nim_model="primary",
        nim_specialist_models={"web.*": "web-model"},
    )).route(_intent("web.search"))

    assert route.model == "web-model"


def test_general_intent_uses_primary_model() -> None:
    route = LlmRouter(Settings(
        nim_model="primary",
        nim_specialist_models={},
    )).route(_intent("chat.general"))

    assert route.model == "primary"
    assert route.requires_generation is True
