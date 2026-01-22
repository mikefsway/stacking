#!/bin/bash
# Quick start script for local testing on Mac/Linux

echo "========================================"
echo "Revenue Stacking Tool - Local Testing"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version

echo ""
echo "[2/3] Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[3/3] Starting Streamlit app..."
echo ""
echo "The app will open in your default browser"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
