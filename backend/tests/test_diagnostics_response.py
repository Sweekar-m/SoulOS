from backend.app.api.v1.diagnostics import DiagnosticsResponse, diagnostics


def test_diagnostics_response_is_typed() -> None:
    response = DiagnosticsResponse(**diagnostics())
    assert response.api == "v1"
    assert isinstance(response.cors_origins, list)
    assert response.total_services >= response.ready_services
