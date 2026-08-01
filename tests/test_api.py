import json
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"


def test_predict_endpoint(client):
    payload = {
        "name": "API Test Project",
        "category": "Infrastructure",
        "budget": 3000000,
        "planned_duration_weeks": 32,
        "team_size": 20,
        "complexity_score": 7.0,
        "contractor_experience_years": 6,
        "scope_changes_count": 2,
        "weather_risk_index": 0.35,
        "supply_chain_delay_score": 0.25
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["project_name"] == "API Test Project"
    assert "prediction" in data
    assert "risk_score" in data["prediction"]


def test_scenario_endpoint(client):
    payload = {
        "base_inputs": { "budget": 1000000, "planned_duration_weeks": 24 },
        "budget_change_pct": 15.0,
        "schedule_change_weeks": 3.0
    }
    res = client.post("/api/scenario", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "scenario_result" in data


def test_weather_endpoint(client):
    res = client.get("/api/weather/forecast?location=Dubai&season=summer&duration_weeks=20")
    assert res.status_code == 200
    data = res.get_json()
    assert data["location"] == "Dubai"


def test_projects_endpoint(client):
    res = client.get("/api/projects")
    assert res.status_code == 200
    data = res.get_json()
    assert "projects" in data


def test_analytics_metrics_endpoint(client):
    res = client.get("/api/analytics/metrics")
    assert res.status_code == 200
    data = res.get_json()
    assert "cost_model_metrics" in data
    assert "schedule_model_metrics" in data

