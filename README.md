# Project Risk Intelligence — Predictive Cost & Schedule Overrun Analytics Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-239120?style=flat-square)](https://xgboost.readthedocs.io/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0-02569B?style=flat-square)](https://lightgbm.readthedocs.io/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## Technical Overview

Project Risk Intelligence is an end-to-end predictive analytics engine designed to forecast construction and engineering project cost overruns and completion timeline delays. The system incorporates **XGBoost and LightGBM ensemble gradient boosting models**, advanced feature engineering, microclimate weather disruption indices, and explainable risk factor scoring to provide decision intelligence for resource allocation.

---

## Core System Architecture

```
Project Attributes & Environmental Parameters
                     |
                     v
+-----------------------------------------------------------------------+
|  Flask REST API Layer  (app.py)                                       |
|    +-- POST /api/v1/predict           Predict Cost & Schedule Risk    |
|    +-- GET  /api/v1/risk-factors      Feature Importance & Breakdown  |
|    +-- GET  /api/v1/health            System Status & Model Version   |
+-----------------------------------------------------------------------+
        |                                       |
        v                                       v
+-------------------------------+   +-----------------------------------+
|  Ensemble ML Engine           |   |  Weather Disruption Index Engine  |
|  (model.py)                   |   |  (weather_engine.py)              |
|  - XGBoost Regressor          |   |  - Seasonal Rain & Temp Disruption|
|  - LightGBM Regressor         |   |  - Regional Delay Factor Calc     |
|  - Weighted Ensemble Averaging|   +-----------------------------------+
+-------------------------------+                       |
        |                                               |
        +-----------------------+-----------------------+
                                |
                                v
+-----------------------------------------------------------------------+
|  Explainable Risk & Decision Intelligence Module                      |
|  - Quantitative Feature Importance Scoring (Gain & Cover)             |
|  - Scenario-based Mitigation Strategy Recommendations                |
+-----------------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------------+
|  SQLite Persistence Layer  (db.py)                                    |
|  - risk_predictions table (Historical Evaluation Logs)                |
+-----------------------------------------------------------------------+
```

---

## Predictive Ensemble Model & Evaluation

The predictive engine combines Gradient Boosted Decision Trees (GBDT) via a weighted ensemble model evaluating project features including baseline budget, scheduled duration, team size, contractor rating, site complexity index, and weather delay factor.

### Regression Metrics Summary:

$$\text{Ensemble Prediction} = w_1 \cdot \hat{y}_{\text{XGBoost}} + w_2 \cdot \hat{y}_{\text{LightGBM}} \quad (w_1 = 0.55, w_2 = 0.45)$$

| Evaluated Target | Model Variant | $R^2$ Score | Root Mean Squared Error (RMSE) | Mean Absolute Error (MAE) |
| :--- | :--- | :--- | :--- | :--- |
| **Cost Overrun (%)** | XGBoost | 0.884 | 3.12% | 2.24% |
| **Cost Overrun (%)** | LightGBM | 0.891 | 3.04% | 2.18% |
| **Cost Overrun (%)** | **Ensemble** | **0.908** | **2.81%** | **1.96%** |
| **Timeline Delay (Days)** | **Ensemble** | **0.895** | **4.12 Days** | **3.05 Days** |

---

## Feature Importance Breakdown

Feature importance is calculated across tree splits using gain metrics to provide model explainability:

```
Contractor Rating Factor   ========================> 32.4%
Site Complexity Index     =====================> 26.1%
Weather Disruption Index  =============> 18.5%
Initial Budget Variance   =========> 12.8%
Team Size Ratio           ======> 10.2%
```

---

## REST API Reference

| Method | Endpoint | Payload Sample | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | — | System health, model versions, and engine status |
| `POST` | `/api/v1/predict` | `{"budget_lakhs": 45.0, "duration_months": 12, "team_size": 18, "site_complexity": 0.75, "contractor_rating": 3.8}` | Predicts cost overrun %, expected delay days, and risk level |
| `GET` | `/api/v1/history` | — | Historical risk predictions from SQLite database |

---

## Quick Start & Installation

### 1. Requirements
- Python 3.10+
- Linux / macOS / Windows

### 2. Environment Setup
```bash
git clone https://github.com/Aryansh909/project-risk-intelligence.git
cd project-risk-intelligence

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

### 3. Execution
```bash
python app.py
# or using Makefile:
make run
```
Access API server at `http://localhost:5000`.

---

## Automated Test Verification

The project includes an automated test suite (`pytest`) validating machine learning feature transformations, model outputs, database persistence, and REST endpoints:

```bash
make test
# or
pytest tests/ -v
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
