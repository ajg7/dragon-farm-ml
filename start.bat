@echo off
REM Dragon Farm ML Service Startup Script for Windows

echo 🐉 Starting Dragon Farm ML Service...

REM Activate virtual environment if it exists
if exist ".venv" (
    echo 📦 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Set environment variables for development
set FLASK_ENV=development
set DEBUG=true
set LOG_LEVEL=DEBUG

REM Run the Flask application
echo 🚀 Starting Flask server...
echo 🌐 Server will be available at: http://localhost:5000
echo 📊 Health check: http://localhost:5000/health
echo 🧬 Breeding API: http://localhost:5000/api/breeding/calculate
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
