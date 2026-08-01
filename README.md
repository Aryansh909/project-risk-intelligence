<div align="center">

![header](https://capsule-render.vercel.app/api?type=rect&color=0:0D1117,100:1A2744&height=90&text=%F0%9F%93%88%20Project%20Risk%20Intelligence&fontSize=28&fontColor=E6EDF3&fontAlignY=55&desc=Cost%20%26%20Schedule%20Overrun%20Prediction%20Engine&descSize=14&descAlignY=78&descColor=7EA8BE)

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=flat-square&logoColor=white)]()
[![LightGBM](https://img.shields.io/badge/LightGBM-02569B?style=flat-square&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-22863A?style=flat-square)](LICENSE)

</div>

---

## Overview

Project Risk Intelligence forecasts construction and infrastructure project cost overruns and schedule delays using an XGBoost + LightGBM ensemble. The core work is in the feature engineering — raw project inputs are transformed into 13 domain-specific risk signals including contractor performance scores, site complexity indices, and seasonal disruption factors. Predictions include feature importance breakdowns and scenario simulation, making it a planning tool rather than a black-box risk score.

## Features

- **Dual prediction targets** — Cost overrun percentage and schedule delay weeks in a single inference pass
- **Ensemble models** — XGBoost + LightGBM with Gradient Boosting and Random Forest fallbacks
- **Domain feature engineering** — 13 derived features from 8 raw project inputs
- **Scenario simulation** — Adjust input parameters and compare risk outcomes side by side
- **CV inspection integration** — Site delay factors sourced from computer vision inspection reports
- **Weather risk engine** — Environmental disruption scoring for outdoor construction projects
- **REST API** — Full JSON API with CORS support

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=flat-square&logoColor=white)]()
[![LightGBM](https://img.shields.io/badge/LightGBM-02569B?style=flat-square&logoColor=white)]()
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)

## Feature Engineering

Raw inputs are engineered into 13 model features:

| Feature | Description |
|:--|:--|
| `budget` | Total project budget |
| `planned_duration_weeks` | Planned timeline |
| `team_size` | Engineering team headcount |
| `complexity_score` | Project complexity rating (1–10) |
| `contractor_experience_years` | Lead contractor track record |
| `scope_changes_count` | Number of scope revisions |
| `weather_risk_index` | Seasonal disruption probability |
| `supply_chain_delay_score` | Material procurement risk |
| `cv_site_delay_factor` | Vision-assessed site delay signal |
| `budget_per_week` | Budget burn rate |
| `budget_per_team` | Resource allocation density |
| `complexity_per_team` | Cognitive load index |
| `risk_pressure_index` | Composite risk pressure signal |

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone https://github.com/Aryansh909/project-risk-intelligence.git
cd project-risk-intelligence
cp .env.example .env
pip install -r requirements.txt
python app.py
```

Dashboard → `http://localhost:5000`

## API Reference

| Method | Endpoint | Description |
|:--|:--|:--|
| `GET` | `/api/health` | Service health check |
| `POST` | `/api/predict` | Predict cost overrun + schedule delay |
| `GET` | `/api/history` | Past prediction history |
| `POST` | `/api/simulate` | Scenario simulation |
| `GET` | `/api/features` | Feature importance breakdown |

## Project Structure

```
project-risk-intelligence/
├── app.py              # Flask application factory, routes
├── model.py            # XGBoost + LightGBM ensemble predictor
├── cv_handler.py       # CV inspection delay factor handler
├── weather_engine.py   # Weather risk scoring engine
├── config.py           # Environment configuration
├── db.py               # SQLite persistence
├── frontend/           # Web dashboard
├── models/             # Saved model weights
├── tests/              # pytest test suite
└── scripts/            # Setup utilities
```

## License

[MIT](LICENSE)
