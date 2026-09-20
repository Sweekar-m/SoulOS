from backend.app.core.config import Settings, settings
from backend.app.intents.models import IntentResult
from backend.app.llm.models import ModelRoute


TOOL_ONLY_INTENTS = {
    "system.open_app",
    "system.close_app",
    "system.screen",
}


class LlmRouter:
    def __init__(self, runtime_settings: Settings = settings) -> None:
        self.settings = runtime_settings

    def route(
        self,
        intent: IntentResult,
        context: dict | None = None,
    ) -> ModelRoute:
        del context

        if intent.intent in TOOL_ONLY_INTENTS:
            return ModelRoute(
                provider="tool-runtime",
                model="",
                reason="system intent is handled by a registered tool",
                requires_generation=False,
            )

        model = self.settings.nim_specialist_models.get(intent.intent)
        if not model:
            family = intent.intent.split(".", maxsplit=1)[0]
            model = self.settings.nim_specialist_models.get(f"{family}.*")
        if not model:
            model = self.settings.nim_model

        return ModelRoute(
            provider="nvidia_nim",
            model=model,
            reason=(
                f"selected NVIDIA NIM model for intent {intent.intent}"
                if model
                else "no NVIDIA NIM model is configured"
            ),
            requires_generation=True,
        )
