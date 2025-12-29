#!/bin/bash
# Run script for Termux on Android

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python solar_predictor.py

