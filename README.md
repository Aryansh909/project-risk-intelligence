# Project Cost & Schedule Risk Prediction Platform

An end-to-end predictive analytics and decision-intelligence platform engineered to forecast project cost overruns and schedule completion delays using ensemble machine learning models, computer vision site inspection, and adverse weather impact modeling.

## Features

- **Ensemble Regression Modeling**: XGBoost and LightGBM models trained on engineered project telemetry features (cost ratios, complexity indices, contractor experience, scope change frequency).
- **Explainable AI (XAI)**: SHAP-equivalent feature contribution breakdowns identifying key risk drivers for every prediction.
- **Scenario Stress Testing**: What-if simulation engine to test project resilience against budget shifts, timeline changes, and supply chain disruptions.
- **Computer Vision Site Inspector**: Image analysis pipeline using OpenCV and Pillow to estimate structural completeness and flag visual delay indicators.
- **Weather Disruption Analytics**: Location and seasonal weather forecasting engine calculating outdoor schedule penalty risks.
- **Interactive Web Dashboard**: Modern glassmorphism single-page web interface built with HTML5, CSS3, and Chart.js.
- **RESTful API Infrastructure**: Flask REST API backed by SQLite persistence layer for managing historical project telemetry.

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                                  Frontend UI                                      |
|            (Vanilla HTML5 / Modern Glassmorphism CSS3 / Chart.js SPA)            |
+----------------------------------------+------------------------------------------+
                                         | REST APIs
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
+-------------------+ +-------------------+ +------------------+ +------------------+
```

## Directory Structure

```
.
├── app.py                  # Flask REST API server and static routing
├── config.py               # Configuration settings and environment management
├── db.py                   # SQLite persistence layer and database schema
├── model.py                # ML pipeline (XGBoost / LightGBM ensemble and SHAP)
├── cv_handler.py           # Computer vision site photo analysis engine
├── weather_engine.py       # Weather risk disruption calculator
├── frontend/               # Single-page application assets (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docs/                   # System architecture and API documentation
│   ├── api_doc.md
│   └── architecture.md
├── scripts/                # Utility and setup scripts
│   ├── setup.sh
│   ├── train_models.py
│   └── seed_db.py
├── tests/                  # Unit test suite (pytest)
│   ├── test_api.py
│   ├── test_config.py
│   ├── test_cv.py
│   ├── test_db.py
│   ├── test_model.py
│   └── test_weather.py
├── .env.example            # Environment configuration template
├── Makefile                # Command automation shortcuts
├── requirements.txt        # Pinned Python dependencies
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Contribution guidelines
└── CHANGELOG.md            # Release version history
```

## Quick Start

### 1. Prerequisites

- Python 3.9+
- virtualenv (recommended)

### 2. Environment Setup

Clone the repository and run the setup script:

```bash
git clone https://github.com/Aryansh909/project-risk-intelligence.git
cd project-risk-intelligence
make setup
```

Alternatively, set up manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 scripts/train_models.py
python3 scripts/seed_db.py
```

### 3. Running the Server

Start the Flask development server:

```bash
make run
```

Access the interactive dashboard at `http://localhost:5000`.

## Testing

Execute the automated test suite:

```bash
make test
```

## REST API Summary

- `GET /api/health`: System health and model initialization status.
- `POST /api/predict`: Predict cost overrun, schedule delay, and risk score.
- `POST /api/scenario`: Run what-if scenario stress testing.
- `POST /api/cv/analyze`: Computer vision photo analysis.
- `GET /api/weather/forecast`: Calculate location-based weather risk.
- `GET /api/projects`: Fetch registered project risk telemetry logs.
- `GET /api/analytics/metrics`: Retrieve cross-validation performance metrics.

For complete API specifications, see `docs/api_doc.md`.

## License

Distributed under the MIT License. See `LICENSE` for details.
