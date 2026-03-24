import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# Use the default dev key for local/CI tests
API_KEY = "startup-intelligence-local-dev-key"
HEADERS = {"x-api-key": API_KEY}

def test_health_check():
    """Verify that the API root is accessible."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_protected_route_fails_without_key():
    """Verify that protected routes return 401 without an API key."""
    response = client.get("/api/discovery/industries")
    assert response.status_code == 401
    assert "Invalid or missing API Key" in response.json()["detail"]

def test_get_industries():
    """Verify that the industries endpoint returns a list of industries."""
    response = client.get("/api/discovery/industries", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_trending_startups():
    """Verify that trending startups endpoint returns valid startup objects."""
    response = client.get("/api/discovery/trending", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        startup = data[0]
        assert "startup_name" in startup
        assert "momentum_score" in startup
        assert "industry" in startup

def test_analytics_trends():
    """Verify that industry trends data is structured correctly."""
    response = client.get("/industry-trends", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "industry_funding" in data
    assert "total_startups" in data
    assert isinstance(data["industry_funding"], list)
