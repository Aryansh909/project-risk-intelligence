# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [1.0.0] - 2026-08-01

### Added
- Initial release of Project Cost & Schedule Risk Prediction Platform.
- Flask REST API backend with project, risk prediction, scenario simulation, computer vision, and weather endpoints.
- SQLite persistence layer for managing historical project risk telemetry.
- Machine Learning pipeline featuring ensemble regression models (XGBoost, LightGBM, Gradient Boosting) for cost overrun ($ and %) and schedule completion delay (weeks) predictions.
- SHAP feature importance explainability breakdown and scenario stress testing engine.
- Computer Vision site inspection photo analysis engine for structural completeness and delay detection.
- Weather forecasting disruption engine for calculating adverse weather penalties on construction timelines.
- Premium glassmorphism interactive web dashboard with real-time sliders, visual dropzone, and Chart.js metrics.
- Comprehensive automated test suite (`pytest`) covering API, DB, model, CV, weather, and configuration modules.
- Setup scripts, Makefile, `.env.example`, MIT License, developer documentation, and architecture specifications.

