import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "up"


def test_info_returns_200(client):
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.get_json()
    assert "time" in data
    assert "hostname" in data
    assert "message" in data
    assert "deployed_on" in data
    assert data["deployed_on"] == "kubernetes"


def test_info_contains_version(client):
    response = client.get("/api/v1/info")
    data = response.get_json()
    assert "version" in data


def test_404_on_unknown_route(client):
    response = client.get("/api/v1/unknown")
    assert response.status_code == 404
