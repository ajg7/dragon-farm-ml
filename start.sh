#!/bin/bash

# Dragon Farm ML Service Startup Script

echo "🐉 Starting Dragon Farm ML Service..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/Scripts/activate
fi

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for development
export FLASK_ENV=development
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run the Flask application
echo "🚀 Starting Flask server..."
echo "🌐 Server will be available at: http://localhost:5000"
echo "📊 Health check: http://localhost:5000/health"
echo "🧬 Breeding API: http://localhost:5000/api/breeding/calculate"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
