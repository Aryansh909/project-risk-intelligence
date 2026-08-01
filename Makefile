.PHONY: help install setup train seed test run clean

help:
	@echo "Available commands:"
	@echo "  make install    Install Python dependencies from requirements.txt"
	@echo "  make setup      Initialize directories and setup environment"
	@echo "  make train      Train XGBoost/LightGBM ML models"
	@echo "  make seed       Seed SQLite database with sample project risk data"
	@echo "  make test       Run automated pytest suite"
	@echo "  make run        Start Flask development API server"
	@echo "  make clean      Remove generated artifacts and database caches"

install:
	pip install -r requirements.txt

setup:
	bash scripts/setup.sh

train:
	python3 scripts/train_models.py

seed:
	python3 scripts/seed_db.py

test:
	PYTHONPATH=. ./venv/bin/pytest tests/ -v

run:
	python3 app.py

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache *.db models/*.joblib uploads/*

