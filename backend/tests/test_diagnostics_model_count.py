from dataclasses import replace

from backend.app.core import diagnostics


def test_snapshot_counts_primary_and_specialist_models(monkeypatch) -> None:
    configured = replace(
        diagnostics.settings,
        nim_model="primary",
        nim_specialist_models={"coding": "specialist", "empty": ""},
    )
    monkeypatch.setattr(diagnostics, "settings", configured)
    value = diagnostics.snapshot()
    assert value.configured_models == 2
