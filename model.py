import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from config import Config

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False


class RiskPredictor:
    """Machine Learning pipeline for predicting project cost overruns and completion delays."""

    FEATURE_NAMES = [
        "budget",
        "planned_duration_weeks",
        "team_size",
        "complexity_score",
        "contractor_experience_years",
        "scope_changes_count",
        "weather_risk_index",
        "supply_chain_delay_score",
        "cv_site_delay_factor",
        "budget_per_week",
        "budget_per_team",
        "complexity_per_team",
        "risk_pressure_index"
    ]

    def __init__(self):
        Config.init_app()
        self.cost_model = None
        self.schedule_model = None
        self.scaler = StandardScaler()
        self._load_or_build_models()

    def engineer_features(self, input_dict):
        """Construct domain-specific features from raw project input."""
        budget = float(input_dict.get("budget", 1000000))
        planned_duration = float(input_dict.get("planned_duration_weeks", 24))
        team_size = float(input_dict.get("team_size", 10))
        complexity = float(input_dict.get("complexity_score", 5.0))
        experience = float(input_dict.get("contractor_experience_years", 5))
        scope_changes = float(input_dict.get("scope_changes_count", 2))
        weather_risk = float(input_dict.get("weather_risk_index", 0.3))
        supply_chain = float(input_dict.get("supply_chain_delay_score", 0.2))
        cv_delay = float(input_dict.get("cv_site_delay_factor", 0.1))

        budget_per_week = budget / max(planned_duration, 1.0)
        budget_per_team = budget / max(team_size, 1.0)
        complexity_per_team = complexity / max(team_size, 1.0)
        risk_pressure = (complexity * 0.3) + (scope_changes * 0.25) + (weather_risk * 15.0) + (supply_chain * 15.0) + (cv_delay * 10.0)

        df = pd.DataFrame([{
            "budget": budget,
            "planned_duration_weeks": planned_duration,
            "team_size": team_size,
            "complexity_score": complexity,
            "contractor_experience_years": experience,
            "scope_changes_count": scope_changes,
            "weather_risk_index": weather_risk,
            "supply_chain_delay_score": supply_chain,
            "cv_site_delay_factor": cv_delay,
            "budget_per_week": budget_per_week,
            "budget_per_team": budget_per_team,
            "complexity_per_team": complexity_per_team,
            "risk_pressure_index": risk_pressure
        }])[self.FEATURE_NAMES]

        return df

    def _create_fallback_models(self):
        """Train baseline fallback models if saved artifacts are absent."""
        np.random.seed(42)
        n_samples = 300
        
        # Synthetic baseline generation
        budgets = np.random.uniform(50000, 10000000, n_samples)
        durations = np.random.randint(4, 104, n_samples)
        teams = np.random.randint(2, 50, n_samples)
        complexities = np.random.uniform(1.0, 10.0, n_samples)
        experiences = np.random.uniform(1.0, 20.0, n_samples)
        scope_changes = np.random.randint(0, 15, n_samples)
        weather_risks = np.random.uniform(0.0, 1.0, n_samples)
        supply_chains = np.random.uniform(0.0, 1.0, n_samples)
        cv_delays = np.random.uniform(0.0, 1.0, n_samples)

        rows = []
        for i in range(n_samples):
            inp = {
                "budget": budgets[i],
                "planned_duration_weeks": durations[i],
                "team_size": teams[i],
                "complexity_score": complexities[i],
                "contractor_experience_years": experiences[i],
                "scope_changes_count": scope_changes[i],
                "weather_risk_index": weather_risks[i],
                "supply_chain_delay_score": supply_chains[i],
                "cv_site_delay_factor": cv_delays[i]
            }
            feat = self.engineer_features(inp)
            rows.append(feat.iloc[0])

        X = pd.DataFrame(rows)[self.FEATURE_NAMES]
        
        # Target formula simulation
        y_cost_pct = (
            (X["complexity_score"] * 2.5) +
            (X["scope_changes_count"] * 3.0) +
            (X["weather_risk_index"] * 18.0) +
            (X["supply_chain_delay_score"] * 22.0) +
            (X["cv_site_delay_factor"] * 15.0) -
            (X["contractor_experience_years"] * 0.8) +
            np.random.normal(0, 2.0, n_samples)
        ).clip(lower=0.0, upper=150.0)

        y_delay_weeks = (
            (X["planned_duration_weeks"] * 0.1) +
            (X["complexity_score"] * 0.8) +
            (X["scope_changes_count"] * 1.2) +
            (X["weather_risk_index"] * 4.0) +
            (X["supply_chain_delay_score"] * 5.0) +
            (X["cv_site_delay_factor"] * 4.0) -
            (X["contractor_experience_years"] * 0.3) +
            np.random.normal(0, 0.5, n_samples)
        ).clip(lower=0.0)

        X_scaled = self.scaler.fit_transform(X)

        if HAS_XGBOOST and HAS_LIGHTGBM:
            cost_xgb = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
            cost_xgb.fit(X_scaled, y_cost_pct)
            cost_lgb = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42, verbose=-1)
            cost_lgb.fit(X_scaled, y_cost_pct)
            self.cost_model = ("ensemble", cost_xgb, cost_lgb)

            sched_xgb = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
            sched_xgb.fit(X_scaled, y_delay_weeks)
            sched_lgb = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42, verbose=-1)
            sched_lgb.fit(X_scaled, y_delay_weeks)
            self.schedule_model = ("ensemble", sched_xgb, sched_lgb)
        else:
            self.cost_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
            self.cost_model.fit(X_scaled, y_cost_pct)

            self.schedule_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
            self.schedule_model.fit(X_scaled, y_delay_weeks)

        # Save artifacts
        joblib.dump(self.cost_model, Config.COST_MODEL_PATH)
        joblib.dump(self.schedule_model, Config.SCHEDULE_MODEL_PATH)
        joblib.dump(self.scaler, Config.SCALER_PATH)

    def _load_or_build_models(self):
        """Load models from disk if available, otherwise train fallback."""
        if (
            os.path.exists(Config.COST_MODEL_PATH) and
            os.path.exists(Config.SCHEDULE_MODEL_PATH) and
            os.path.exists(Config.SCALER_PATH)
        ):
            try:
                self.cost_model = joblib.load(Config.COST_MODEL_PATH)
                self.schedule_model = joblib.load(Config.SCHEDULE_MODEL_PATH)
                self.scaler = joblib.load(Config.SCALER_PATH)
            except Exception:
                self._create_fallback_models()
        else:
            self._create_fallback_models()

    def _predict_raw(self, X_scaled, model_obj):
        """Internal helper for ensemble vs single model inference."""
        if isinstance(model_obj, tuple) and model_obj[0] == "ensemble":
            pred1 = model_obj[1].predict(X_scaled)
            pred2 = model_obj[2].predict(X_scaled)
            return (pred1 + pred2) / 2.0
        return model_obj.predict(X_scaled)

    def predict(self, input_dict):
        """Execute risk prediction and feature contribution breakdown."""
        df_feat = self.engineer_features(input_dict)
        X_scaled = self.scaler.transform(df_feat)

        cost_overrun_pct = float(np.maximum(0.0, self._predict_raw(X_scaled, self.cost_model)[0]))
        budget = float(input_dict.get("budget", 1000000))
        cost_overrun_amount = float((cost_overrun_pct / 100.0) * budget)

        delay_weeks = float(np.maximum(0.0, self._predict_raw(X_scaled, self.schedule_model)[0]))

        # Calculate Risk Score (0-100)
        # Combination of cost overrun %, delay ratio, and risk pressure index
        planned_weeks = max(1.0, float(input_dict.get("planned_duration_weeks", 24)))
        delay_ratio = delay_weeks / planned_weeks
        raw_risk = (cost_overrun_pct * 0.45) + (delay_ratio * 100 * 0.35) + (df_feat["risk_pressure_index"].iloc[0] * 0.2)
        risk_score = float(np.clip(raw_risk, 0.0, 100.0))

        if risk_score < 25:
            risk_category = "Low"
        elif risk_score < 50:
            risk_category = "Medium"
        elif risk_score < 75:
            risk_category = "High"
        else:
            risk_category = "Critical"

        # Feature Importance / SHAP-style Explainability calculation
        contributions = self._compute_feature_contributions(df_feat.iloc[0])
        recommendations = self._generate_recommendations(df_feat.iloc[0], risk_category, cost_overrun_pct, delay_weeks)

        return {
            "predicted_cost_overrun_pct": round(cost_overrun_pct, 2),
            "predicted_cost_overrun_amount": round(cost_overrun_amount, 2),
            "predicted_delay_weeks": round(delay_weeks, 1),
            "risk_score": round(risk_score, 1),
            "risk_category": risk_category,
            "feature_contributions": contributions,
            "recommendations": recommendations
        }

    def _compute_feature_contributions(self, row):
        """Compute relative percentage impact of input features on overall risk."""
        weights = {
            "supply_chain_delay_score": row["supply_chain_delay_score"] * 25.0,
            "weather_risk_index": row["weather_risk_index"] * 22.0,
            "scope_changes_count": (row["scope_changes_count"] / 10.0) * 18.0,
            "complexity_score": (row["complexity_score"] / 10.0) * 15.0,
            "cv_site_delay_factor": row["cv_site_delay_factor"] * 12.0,
            "contractor_experience": max(0, 15 - row["contractor_experience_years"]) * 0.8
        }
        total_w = sum(weights.values()) if sum(weights.values()) > 0 else 1.0
        return {k: round((v / total_w) * 100.0, 1) for k, v in sorted(weights.items(), key=lambda x: x[1], reverse=True)}

    def _generate_recommendations(self, row, category, cost_pct, delay_w):
        """Generate targeted risk mitigation strategies."""
        recs = []
        if row["supply_chain_delay_score"] > 0.4:
            recs.append("Diversify critical materials suppliers to buffer against supply chain lags.")
        if row["weather_risk_index"] > 0.5:
            recs.append("Schedule outdoor activities during low-risk seasonal weather windows.")
        if row["scope_changes_count"] > 3:
            recs.append("Establish strict scope freeze milestones and change-control board approvals.")
        if row["complexity_score"] > 7.0:
            recs.append("Increase expert engineering review frequency and allocate secondary contingency budget.")
        if row["contractor_experience_years"] < 3:
            recs.append("Assign a senior advisory supervisor to guide project execution team.")

        if not recs:
            recs.append("Maintain baseline project management protocols and periodic status reporting.")
        return recs

    def simulate_scenario(self, base_inputs, budget_change_pct=0.0, schedule_change_weeks=0.0, weather_factor_delta=0.0, supply_chain_delta=0.0):
        """Run what-if scenario stress testing."""
        scenario_inputs = base_inputs.copy()
        
        orig_budget = float(base_inputs.get("budget", 1000000))
        scenario_inputs["budget"] = orig_budget * (1.0 + (budget_change_pct / 100.0))

        orig_duration = float(base_inputs.get("planned_duration_weeks", 24))
        scenario_inputs["planned_duration_weeks"] = max(1, orig_duration + schedule_change_weeks)

        orig_weather = float(base_inputs.get("weather_risk_index", 0.3))
        scenario_inputs["weather_risk_index"] = float(np.clip(orig_weather + weather_factor_delta, 0.0, 1.0))

        orig_sc = float(base_inputs.get("supply_chain_delay_score", 0.2))
        scenario_inputs["supply_chain_delay_score"] = float(np.clip(orig_sc + supply_chain_delta, 0.0, 1.0))

        return self.predict(scenario_inputs)

