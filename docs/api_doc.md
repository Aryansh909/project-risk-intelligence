# REST API Documentation

The Project Cost & Schedule Risk Prediction API exposes endpoints for risk calculation, what-if stress testing, computer vision image analysis, weather forecasting, and database telemetry.

## Base URL
`http://localhost:5000/api`

---

### 1. Health Check
- **Endpoint**: `GET /api/health`
- **Response**:
```json
{
  "status": "healthy",
  "service": "Project Cost & Schedule Risk Prediction API",
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true,
  "models_loaded": true
}
```

---

### 2. Risk Prediction
- **Endpoint**: `POST /api/predict`
- **Request Body**:
```json
{
  "name": "Highway Overpass Project",
  "category": "Infrastructure",
  "budget": 5000000,
  "planned_duration_weeks": 36,
  "team_size": 25,
  "complexity_score": 7.5,
  "contractor_experience_years": 8,
  "scope_changes_count": 3,
  "weather_risk_index": 0.4,
  "supply_chain_delay_score": 0.3
}
```
- **Response**:
```json
{
  "project_id": 1,
  "project_name": "Highway Overpass Project",
  "category": "Infrastructure",
  "prediction": {
    "predicted_cost_overrun_pct": 18.5,
    "predicted_cost_overrun_amount": 925000.0,
    "predicted_delay_weeks": 4.2,
    "risk_score": 62.1,
    "risk_category": "High",
    "feature_contributions": {
      "SUPPLY_CHAIN_DELAY_SCORE": 28.5,
      "WEATHER_RISK_INDEX": 24.1
    },
    "recommendations": [
      "Diversify critical materials suppliers to buffer against supply chain lags."
    ]
  }
}
```

---

### 3. What-If Scenario Stress Testing
- **Endpoint**: `POST /api/scenario`
- **Request Body**:
```json
{
  "base_inputs": { "budget": 1000000, "planned_duration_weeks": 24 },
  "budget_change_pct": 10.0,
  "schedule_change_weeks": 4.0,
  "weather_factor_delta": 0.2,
  "scenario_name": "High Severe Weather Scenario"
}
```

---

### 4. Computer Vision Image Analysis
- **Endpoint**: `POST /api/cv/analyze`
- **Content-Type**: `multipart/form-data`
- **Form Parameters**:
  - `image`: File attachment (PNG/JPEG)
  - `project_id`: (Optional) Integer ID

---

### 5. Weather Forecast Risk
- **Endpoint**: `GET /api/weather/forecast?location=London&season=winter&duration_weeks=30`

---

### 6. Projects & Analytics
- `GET /api/projects`: List registered projects and risk histories.
- `GET /api/analytics/metrics`: Retrieve validation performance metrics (R2, MAE, RMSE).

