import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage_loads(client):
    """Homepage should return 200 OK"""
    response = client.get("/")
    assert response.status_code == 200

def test_health_endpoint(client):
    """Health endpoint must return healthy status for Docker HEALTHCHECK"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

def test_api_destinations(client):
    """API should return list of destinations"""
    response = client.get("/api/destinations")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "country" in data[0]
    assert "price" in data[0]

def test_destinations_count(client):
    """Should have exactly 6 destinations"""
    response = client.get("/api/destinations")
    data = response.get_json()
    assert len(data) == 6

def test_homepage_contains_destinations(client):
    """Homepage HTML should contain destination names"""
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Santorini" in html
    assert "Kyoto" in html
    assert "WanderLust" in html
