from fastapi.testclient import TestClient

from backend.app.main import app


def test_models_catalog_exposes_metadata_only() -> None:
    response = TestClient(app).get("/api/v1/models")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["models"], list)
    for model in body["models"]:
        assert {"provider", "model", "role"}.issubset(model)
        assert "api_key" not in model
