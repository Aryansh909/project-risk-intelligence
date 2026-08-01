# Architecture & System Design Specification

## Overview

The Project Cost & Schedule Risk Prediction Platform is built on a modular decision-intelligence architecture combining ML regression modeling, computer vision site inspection, weather disruption analytics, and an interactive web dashboard.

## System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  Frontend UI                                      |
|            (Vanilla HTML5 / Modern Glassmorphism CSS3 / Chart.js SPA)            |
+----------------------------------------+------------------------------------------+
                                         | REST APIs (JSON / FormData)
                                         v
+-----------------------------------------------------------------------------------+
|                                 Flask REST Server                                 |
|                                    (app.py)                                       |
+-----------+-------------------+-------------------+-------------------+-----------+
            |                   |                   |                   |
            v                   v                   v                   v
+-------------------+ +-------------------+ +------------------+ +------------------+
|    ML Pipeline    | | Computer Vision   | |  Weather Engine  | | SQLite Database  |
|    (model.py)     | | (cv_handler.py)   | |(weather_engine)| |    (db.py)       |
|  XGBoost/LightGBM | | OpenCV / Pillow   | | Disruption Index | | Project Logs &   |
|   SHAP Explain    | | Site Inspection | | Seasonal Model | | Telemetry Data   |
+-------------------+ +-------------------+ +------------------+ +------------------+
```

## Modular Breakdown

1. **ML Risk Pipeline (`model.py`)**:
   - Uses ensemble XGBoost and LightGBM regressors to output continuous target variables (`predicted_cost_overrun_pct`, `predicted_delay_weeks`).
   - Feature engineering transforms raw inputs into domain metrics (`budget_per_week`, `complexity_per_team`, `risk_pressure_index`).
   - Computes SHAP-equivalent feature contribution breakdowns for explainable AI.

2. **Computer Vision Inspection (`cv_handler.py`)**:
   - Parses construction site photos using OpenCV edge density, color distribution, brightness/contrast, and texture metrics to calculate structural completeness & risk factors.

3. **Weather Disruption Engine (`weather_engine.py`)**:
   - Models location-specific seasonal adverse weather days (rain, extreme wind, snow) and computes schedule impact penalties.

4. **Persistence Layer (`db.py`)**:
   - SQLite relational schema tracking projects, prediction runs, site photo analysis logs, weather forecasts, and scenario stress-test outputs.
