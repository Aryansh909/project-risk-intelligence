import math
import numpy as np


class WeatherEngine:
    """Weather forecasting and outdoor risk modeling engine."""

    # Seasonal baseline disruption risk factors (Northern hemisphere default)
    SEASON_RISK_MAP = {
        "winter": 0.65,
        "spring": 0.40,
        "summer": 0.20,
        "fall": 0.35
    }

    LOCATION_PRESET_MAP = {
        "new york": {"base_rain_days": 110, "extreme_wind_days": 12, "snow_days": 20},
        "london": {"base_rain_days": 150, "extreme_wind_days": 18, "snow_days": 5},
        "singapore": {"base_rain_days": 170, "extreme_wind_days": 5, "snow_days": 0},
        "dubai": {"base_rain_days": 25, "extreme_wind_days": 15, "snow_days": 0},
        "tokyo": {"base_rain_days": 115, "extreme_wind_days": 10, "snow_days": 8},
        "sydney": {"base_rain_days": 100, "extreme_wind_days": 14, "snow_days": 0},
        "default": {"base_rain_days": 90, "extreme_wind_days": 10, "snow_days": 5}
    }

    def __init__(self):
        pass

    def evaluate_weather_risk(self, location="New York, USA", season="spring", duration_weeks=24):
        """Calculate weather risk index, projected adverse days, and schedule impact penalty."""
        loc_key = location.lower().split(",")[0].strip()
        loc_data = self.LOCATION_PRESET_MAP.get(loc_key, self.LOCATION_PRESET_MAP["default"])

        season_factor = self.SEASON_RISK_MAP.get(season.lower(), 0.35)

        # Annualized adverse weather ratio
        total_adverse_annual = loc_data["base_rain_days"] + (loc_data["extreme_wind_days"] * 1.2) + (loc_data["snow_days"] * 1.5)
        annual_adverse_ratio = total_adverse_annual / 365.0

        # Project duration scaling
        duration_days = duration_weeks * 7
        adverse_days_projected = int(round(duration_days * annual_adverse_ratio * (0.8 + season_factor)))

        # Schedule penalty calculation (5 workdays per week baseline)
        schedule_penalty_weeks = round(adverse_days_projected / 5.0 * 0.4, 1)

        # Weather Risk Index (0.0 to 1.0)
        raw_index = (annual_adverse_ratio * 0.5) + (season_factor * 0.3) + (min(schedule_penalty_weeks, 10.0) / 10.0 * 0.2)
        weather_risk_index = round(float(np.clip(raw_index, 0.05, 0.95)), 2)

        if weather_risk_index < 0.3:
            severity = "Low"
            mitigation = "Favorable weather conditions projected. Standard site operations."
        elif weather_risk_index < 0.6:
            severity = "Moderate"
            mitigation = "Potential rain or wind slowdowns. Maintain temporary shelter canvas."
        else:
            severity = "High"
            mitigation = "High risk of seasonal weather disruptions. Pre-order weather-resistant materials and plan indoor work buffer shifts."

        return {
            "location": location,
            "season": season,
            "weather_risk_index": weather_risk_index,
            "severity": severity,
            "adverse_days_projected": adverse_days_projected,
            "schedule_penalty_weeks": schedule_penalty_weeks,
            "mitigation_advice": mitigation
        }
