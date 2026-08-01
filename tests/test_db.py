import os
import pytest
from db import Database


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_db.db"
    db = Database(db_file)
    db.init_db()
    return db


def test_init_db_creates_tables(temp_db):
    conn = temp_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    assert "projects" in tables
    assert "predictions" in tables
    assert "site_images" in tables
    assert "weather_logs" in tables
    assert "scenario_simulations" in tables


def test_project_crud(temp_db):
    project_id = temp_db.create_project(
        name="Test Transit System",
        category="Infrastructure",
        budget=1500000.0,
        planned_duration_weeks=30,
        team_size=15,
        complexity_score=6.0
    )
    assert project_id == 1

    project = temp_db.get_project(project_id)
    assert project["name"] == "Test Transit System"
    assert project["budget"] == 1500000.0

    all_projects = temp_db.get_all_projects()
    assert len(all_projects) == 1


def test_save_prediction(temp_db):
    project_id = temp_db.create_project("Test", "Category", 1000, 10, 5, 5.0)
    pred_id = temp_db.save_prediction(
        project_id=project_id,
        cost_overrun_pct=15.5,
        cost_overrun_amount=155.0,
        delay_weeks=2.0,
        risk_score=45.0,
        risk_category="Medium",
        feature_contributions={"weather": 40.0},
        recommendations=["Buffer schedule"]
    )
    assert pred_id == 1

    latest = temp_db.get_latest_prediction(project_id)
    assert latest["predicted_cost_overrun_pct"] == 15.5
    assert latest["risk_category"] == "Medium"
