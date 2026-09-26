from backend.app.tools.presentation import PresentationTool


def test_presentation_limits_slide_count():
    tool = PresentationTool()
    validated = tool.validate({"topic": "AI", "slides": 12})
    assert validated.slides == 12


def test_presentation_rejects_unbounded_slide_count():
    try:
        PresentationTool().validate({"topic": "AI", "slides": 31})
    except Exception:
        return
    raise AssertionError("slide count should be bounded")
