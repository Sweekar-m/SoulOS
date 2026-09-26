from backend.app.tools.search import WebSearchTool


def test_search_rejects_oversized_queries():
    tool = WebSearchTool()
    try:
        tool.validate({"query": "x" * 501})
    except Exception:
        return
    raise AssertionError("oversized query should be rejected")


def test_search_never_executes_unvalidated_input():
    result = WebSearchTool().execute(WebSearchTool().validate({"query": "SoulOS", "limit": 3}))
    assert result.success is False
    assert result.output["limit"] == 3
