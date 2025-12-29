#!/bin/bash
# Run script for desktop environments (Linux/macOS)

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment and run
source venv/bin/activate
python solar_predictor.py

