import os
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig


def test_config_defaults():
    assert Config.PORT == 5000
    assert Config.DB_NAME == "risk_intelligence.db"
    assert "png" in Config.ALLOWED_IMAGE_EXTENSIONS


def test_testing_config():
    assert TestingConfig.TESTING is True
    assert TestingConfig.DEBUG is False
    assert "test_" in TestingConfig.DB_NAME

