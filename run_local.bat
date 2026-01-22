@echo off
REM Quick start script for local testing on Windows

echo ========================================
echo Revenue Stacking Tool - Local Testing
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/3] Starting Streamlit app...
echo.
echo The app will open in your default browser
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
