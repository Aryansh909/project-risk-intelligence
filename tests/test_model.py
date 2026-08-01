import pytest
from model import RiskPredictor


@pytest.fixture
def predictor():
    return RiskPredictor()


def test_feature_engineering(predictor):
    inp = {
        "budget": 2000000,
        "planned_duration_weeks": 40,
        "team_size": 20,
        "complexity_score": 7.0
    }
    df = predictor.engineer_features(inp)
    assert "budget_per_week" in df.columns
    assert "risk_pressure_index" in df.columns
    assert df["budget_per_week"].iloc[0] == 50000.0


def test_prediction_output_structure(predictor):
    inp = {
        "budget": 1000000,
        "planned_duration_weeks": 24,
        "team_size": 10,
        "complexity_score": 6.5,
        "contractor_experience_years": 5,
        "scope_changes_count": 2,
        "weather_risk_index": 0.3,
        "supply_chain_delay_score": 0.2
    }
    res = predictor.predict(inp)
    assert "predicted_cost_overrun_pct" in res
    assert "predicted_cost_overrun_amount" in res
    assert "predicted_delay_weeks" in res
    assert "risk_score" in res
    assert res["risk_category"] in ["Low", "Medium", "High", "Critical"]
    assert isinstance(res["feature_contributions"], dict)
    assert isinstance(res["recommendations"], list)


def test_scenario_simulation(predictor):
    base_inp = {
        "budget": 1000000,
        "planned_duration_weeks": 24,
        "complexity_score": 5.0
    }
    sim_res = predictor.simulate_scenario(
        base_inputs=base_inp,
        budget_change_pct=20.0,
        schedule_change_weeks=6.0,
        weather_factor_delta=0.3
    )
    assert "risk_score" in sim_res

