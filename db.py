import sqlite3
import json
from datetime import datetime, timezone
from config import Config


class Database:
    """SQLite Database manager for project risk intelligence system."""

    def __init__(self, db_path=None):
        self.db_path = str(db_path or Config.DB_PATH)

    def get_connection(self):
        """Get a new SQLite connection with dictionary row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize SQLite database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Projects Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    budget REAL NOT NULL,
                    planned_duration_weeks INTEGER NOT NULL,
                    team_size INTEGER NOT NULL,
                    complexity_score REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Predictions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    predicted_cost_overrun_pct REAL NOT NULL,
                    predicted_cost_overrun_amount REAL NOT NULL,
                    predicted_delay_weeks REAL NOT NULL,
                    risk_score REAL NOT NULL,
                    risk_category TEXT NOT NULL,
                    feature_contributions TEXT,
                    recommendations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                );
            """)

            # Site Images Table (CV Analysis)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS site_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    completeness_score REAL NOT NULL,
                    structural_risk_score REAL NOT NULL,
                    detected_anomalies TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                );
            """)

            # Weather Disruption Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    disruption_index REAL NOT NULL,
                    adverse_days_projected INTEGER NOT NULL,
                    schedule_penalty_weeks REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Scenario Simulations Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scenario_simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    scenario_name TEXT NOT NULL,
                    budget_change_pct REAL NOT NULL,
                    schedule_change_weeks REAL NOT NULL,
                    weather_factor REAL NOT NULL,
                    supply_chain_delay_weeks REAL NOT NULL,
                    simulated_cost_overrun_pct REAL NOT NULL,
                    simulated_delay_weeks REAL NOT NULL,
                    simulated_risk_score REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
                );
            """)

            conn.commit()

    def create_project(self, name, category, budget, planned_duration_weeks, team_size, complexity_score):
        """Insert a new project record."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (name, category, budget, planned_duration_weeks, team_size, complexity_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, category, float(budget), int(planned_duration_weeks), int(team_size), float(complexity_score)))
            conn.commit()
            return cursor.lastrowid

    def get_project(self, project_id):
        """Fetch project by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_projects(self):
        """Retrieve list of all projects with latest risk prediction summary."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*, 
                       pr.risk_score, 
                       pr.risk_category, 
                       pr.predicted_cost_overrun_pct, 
                       pr.predicted_delay_weeks
                FROM projects p
                LEFT JOIN (
                    SELECT project_id, risk_score, risk_category, predicted_cost_overrun_pct, predicted_delay_weeks,
                           ROW_NUMBER() OVER (PARTITION BY project_id ORDER BY created_at DESC) as rn
                    FROM predictions
                ) pr ON p.id = pr.project_id AND pr.rn = 1
                ORDER BY p.created_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def save_prediction(self, project_id, cost_overrun_pct, cost_overrun_amount, delay_weeks, risk_score, risk_category, feature_contributions, recommendations):
        """Save a prediction result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            contrib_json = json.dumps(feature_contributions) if isinstance(feature_contributions, (dict, list)) else feature_contributions
            recs_json = json.dumps(recommendations) if isinstance(recommendations, (dict, list)) else recommendations

            cursor.execute("""
                INSERT INTO predictions (
                    project_id, predicted_cost_overrun_pct, predicted_cost_overrun_amount,
                    predicted_delay_weeks, risk_score, risk_category, feature_contributions, recommendations
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (project_id, float(cost_overrun_pct), float(cost_overrun_amount), float(delay_weeks),
                  float(risk_score), risk_category, contrib_json, recs_json))
            conn.commit()
            return cursor.lastrowid

    def get_latest_prediction(self, project_id):
        """Get latest prediction for a project."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM predictions WHERE project_id = ? ORDER BY created_at DESC LIMIT 1", (project_id,))
            row = cursor.fetchone()
            if row:
                res = dict(row)
                res["feature_contributions"] = json.loads(res["feature_contributions"]) if res["feature_contributions"] else {}
                res["recommendations"] = json.loads(res["recommendations"]) if res["recommendations"] else []
                return res
            return None

    def save_site_image_analysis(self, project_id, filename, file_path, completeness_score, structural_risk_score, detected_anomalies):
        """Save computer vision image analysis result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            anomalies_json = json.dumps(detected_anomalies) if isinstance(detected_anomalies, (dict, list)) else detected_anomalies
            cursor.execute("""
                INSERT INTO site_images (project_id, filename, file_path, completeness_score, structural_risk_score, detected_anomalies)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (project_id, filename, file_path, float(completeness_score), float(structural_risk_score), anomalies_json))
            conn.commit()
            return cursor.lastrowid

    def save_weather_log(self, location, disruption_index, adverse_days_projected, schedule_penalty_weeks):
        """Log weather risk assessment."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO weather_logs (location, disruption_index, adverse_days_projected, schedule_penalty_weeks)
                VALUES (?, ?, ?, ?)
            """, (location, float(disruption_index), int(adverse_days_projected), float(schedule_penalty_weeks)))
            conn.commit()
            return cursor.lastrowid

    def save_scenario(self, project_id, scenario_name, budget_change_pct, schedule_change_weeks, weather_factor, supply_chain_delay_weeks, simulated_cost_overrun_pct, simulated_delay_weeks, simulated_risk_score):
        """Save scenario simulation run."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scenario_simulations (
                    project_id, scenario_name, budget_change_pct, schedule_change_weeks,
                    weather_factor, supply_chain_delay_weeks, simulated_cost_overrun_pct,
                    simulated_delay_weeks, simulated_risk_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (project_id, scenario_name, float(budget_change_pct), float(schedule_change_weeks),
                  float(weather_factor), float(supply_chain_delay_weeks), float(simulated_cost_overrun_pct),
                  float(simulated_delay_weeks), float(simulated_risk_score)))
            conn.commit()
            return cursor.lastrowid
