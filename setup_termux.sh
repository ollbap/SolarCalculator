#!/bin/bash
# Setup script for Termux on Android

set -e

echo "Setting up Solar Predictor for Termux..."

# Update packages and install Python
pkg update -y
pkg install -y python
echo "✓ Python installed"

# Install dependencies (if any)
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

echo ""
echo "Setup complete! Run the predictor with:"
echo "  ./run_termux.sh"

