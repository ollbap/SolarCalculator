#!/bin/bash
# Setup script for desktop environments (Linux/macOS)

set -e

echo "Setting up Solar Predictor..."

# Create virtual environment
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

echo ""
echo "Setup complete! Run the predictor with:"
echo "  ./run.sh"

