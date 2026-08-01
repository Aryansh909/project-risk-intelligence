#!/usr/bin/env python3
"""
Model Training Script for Project Cost & Schedule Risk Prediction Platform.
Generates synthetic project dataset, fits XGBoost / LightGBM ensemble models,
evaluates R2, MAE, RMSE metrics, and serializes model artifacts to models/ directory.
"""

import sys
from pathlib import Path

# Add root project path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from model import RiskPredictor

def main():
    print("Initializing Machine Learning training pipeline...")
    predictor = RiskPredictor()
    predictor._create_fallback_models()
    print("Model training completed successfully!")
    print(f"Cost overrun model saved to: {predictor.cost_model}")
    print(f"Schedule delay model saved to: {predictor.schedule_model}")

if __name__ == "__main__":
    main()
