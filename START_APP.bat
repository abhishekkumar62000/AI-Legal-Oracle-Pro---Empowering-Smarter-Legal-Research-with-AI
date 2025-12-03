@echo off
echo ================================================
echo    AI Legal Oracle - Starting Application
echo ================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking environment...
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create .env file with your OpenAI API key
    pause
    exit /b 1
)

echo [2/3] Navigating to app directory...
echo Current directory: %CD%

echo [3/3] Starting Streamlit app...
echo.
echo ================================================
echo  App will open in your browser automatically
echo  URL: http://localhost:8501
echo ================================================
echo.
echo Press Ctrl+C to stop the app
echo.

streamlit run app_stable.py

pause
