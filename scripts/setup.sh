#!/usr/bin/env bash
# Automated Setup Script for Project Cost & Schedule Risk Prediction Platform

set -e

echo "=== Setting up Project Cost & Schedule Risk Prediction Platform ==="

# Check Python version
python3 -c "import sys; print(f'Python Version: {sys.version}')"

# Create virtualenv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || true
fi

# Activate virtualenv if present
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Upgrade pip and install requirements
echo "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Train models
echo "Training ML Models..."
python3 scripts/train_models.py

# Seed database
echo "Seeding SQLite database..."
python3 scripts/seed_db.py

echo "=== Setup completed successfully! Run 'make run' or 'python3 app.py' to start the server ==="
