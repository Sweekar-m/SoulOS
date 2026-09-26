from backend.app.tools.catalog import builtin_tools


def test_builtin_catalog_has_explicit_core_tools():
    names = [tool.name for tool in builtin_tools()]
    assert names == ["system.open_app", "web.search", "presentation.generate"]


def test_builtin_catalog_metadata_is_schema_driven():
    for tool in builtin_tools():
        metadata = tool.metadata()
        assert metadata["name"] == tool.name
        assert "properties" in metadata["arguments"]
