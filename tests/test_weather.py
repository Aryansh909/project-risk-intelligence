from weather_engine import WeatherEngine


def test_weather_evaluation():
    engine = WeatherEngine()
    res = engine.evaluate_weather_risk(
        location="London",
        season="winter",
        duration_weeks=30
    )
    assert res["location"] == "London"
    assert res["season"] == "winter"
    assert 0.0 <= res["weather_risk_index"] <= 1.0
    assert res["adverse_days_projected"] >= 0
    assert res["schedule_penalty_weeks"] >= 0.0
    assert "mitigation_advice" in res

