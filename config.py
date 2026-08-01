import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if available
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration management class."""

    SECRET_KEY = os.getenv("SECRET_KEY", "default-risk-intelligence-secret-key-2026")
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # Database Configuration
    DB_NAME = os.getenv("DB_NAME", "risk_intelligence.db")
    DB_PATH = BASE_DIR / DB_NAME
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

    # Directory Paths
    MODELS_DIR = BASE_DIR / "models"
    UPLOADS_DIR = BASE_DIR / "uploads"
    FRONTEND_DIR = BASE_DIR / "frontend"
    DOCS_DIR = BASE_DIR / "docs"

    # ML Model Artifacts
    COST_MODEL_PATH = MODELS_DIR / "cost_overrun_model.joblib"
    SCHEDULE_MODEL_PATH = MODELS_DIR / "schedule_delay_model.joblib"
    SCALER_PATH = MODELS_DIR / "feature_scaler.joblib"

    # Computer Vision Settings
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    MAX_IMAGE_SIZE_MB = 16

    # Weather API Settings
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "simulated_key")
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "New York, USA")

    @classmethod
    def init_app(cls, app=None):
        """Ensure necessary runtime directories exist."""
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    DB_NAME = "test_risk_intelligence.db"
    DB_PATH = BASE_DIR / "test_risk_intelligence.db"


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
