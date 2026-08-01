#!/usr/bin/env python3
"""
Database Seeding Script for Project Cost & Schedule Risk Prediction Platform.
Populates SQLite database with sample historical projects and risk predictions.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from db import Database
from model import RiskPredictor

SAMPLE_PROJECTS = [
    {
        "name": "Hudson Yards Commercial Tower Phase II",
        "category": "Commercial Construction",
        "budget": 12500000.0,
        "planned_duration_weeks": 52,
        "team_size": 45,
        "complexity_score": 8.5,
        "contractor_experience_years": 12,
        "scope_changes_count": 5,
        "weather_risk_index": 0.45,
        "supply_chain_delay_score": 0.40
    },
    {
        "name": "Suburban Solar Farm Energy Grid",
        "category": "Energy & Utilities",
        "budget": 4200000.0,
        "planned_duration_weeks": 28,
        "team_size": 20,
        "complexity_score": 5.0,
        "contractor_experience_years": 8,
        "scope_changes_count": 1,
        "weather_risk_index": 0.20,
        "supply_chain_delay_score": 0.15
    },
    {
        "name": "Downtown Highway Overpass Rehabilitation",
        "category": "Infrastructure",
        "budget": 8700000.0,
        "planned_duration_weeks": 40,
        "team_size": 30,
        "complexity_score": 7.8,
        "contractor_experience_years": 5,
        "scope_changes_count": 4,
        "weather_risk_index": 0.60,
        "supply_chain_delay_score": 0.55
    },
    {
        "name": "Cloud Data Center Modernization",
        "category": "Software & IT",
        "budget": 1800000.0,
        "planned_duration_weeks": 16,
        "team_size": 12,
        "complexity_score": 4.2,
        "contractor_experience_years": 10,
        "scope_changes_count": 0,
        "weather_risk_index": 0.10,
        "supply_chain_delay_score": 0.10
    }
]

def main():
    print("Initializing SQLite database seeder...")
    db = Database()
    db.init_db()
    predictor = RiskPredictor()

    for p in SAMPLE_PROJECTS:
        proj_id = db.create_project(
            name=p["name"],
            category=p["category"],
            budget=p["budget"],
            planned_duration_weeks=p["planned_duration_weeks"],
            team_size=p["team_size"],
            complexity_score=p["complexity_score"]
        )

        res = predictor.predict(p)

        db.save_prediction(
            project_id=proj_id,
            cost_overrun_pct=res["predicted_cost_overrun_pct"],
            cost_overrun_amount=res["predicted_cost_overrun_amount"],
            delay_weeks=res["predicted_delay_weeks"],
            risk_score=res["risk_score"],
            risk_category=res["risk_category"],
            feature_contributions=res["feature_contributions"],
            recommendations=res["recommendations"]
        )
        print(f"Seeded project: '{p['name']}' (ID: {proj_id}) | Risk: {res['risk_category']} ({res['risk_score']}/100)")

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    main()

