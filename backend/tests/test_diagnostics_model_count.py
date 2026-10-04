from backend.app.core import diagnostics


def test_snapshot_counts_primary_and_specialist_models(monkeypatch) -> None:
    monkeypatch.setattr(diagnostics.settings, "nim_model", "primary")
    monkeypatch.setattr(
        diagnostics.settings,
        "nim_specialist_models",
        {"coding": "specialist", "empty": ""},
    )
    value = diagnostics.snapshot()
    assert value.configured_models == 2
