from backend.app.intents.classifier import IntentClassifier


def test_exact_and_paraphrased_commands_route_to_expected_intents() -> None:
    classifier = IntentClassifier()
    assert classifier.predict("open chrome")[0] == "system.open_app"
    assert classifier.predict("make me some powerpoint slides")[0] == "presentation.generate"
    assert classifier.predict("search online for this")[0] == "web.search"


def test_unknown_text_has_low_confidence() -> None:
    classifier = IntentClassifier()
    _, confidence = classifier.predict("zzzz qqqq completely unrelated")
    assert confidence < 0.52
