from .catalog import CONFIDENCE_THRESHOLD, DESTRUCTIVE_INTENTS
from .classifier import IntentClassifier
from .entities import extract_entities
from .models import IntentResult


class IntentService:
    def __init__(self, classifier: IntentClassifier | None = None) -> None:
        self.classifier = classifier or IntentClassifier()

    def classify(self, text: str) -> IntentResult:
        normalized = " ".join(text.strip().split())
        intent, confidence = self.classifier.predict(normalized)
        if confidence < CONFIDENCE_THRESHOLD:
            intent = "unknown"
        entities = extract_entities(normalized, intent)
        requires_confirmation = intent in DESTRUCTIVE_INTENTS and confidence < 0.85
        return IntentResult(
            intent=intent,
            confidence=confidence,
            entities=entities,
            requires_confirmation=requires_confirmation,
        )
