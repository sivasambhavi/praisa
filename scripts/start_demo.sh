#!/bin/bash
# PRAISA Demo Startup Script
# 
# This script starts the PRAISA backend server for demo purposes.
# Usage: ./scripts/start_demo.sh (Linux/Mac) or bash scripts/start_demo.sh (Windows Git Bash)

echo "========================================="
echo "PRAISA - Starting Demo Server"
echo "========================================="
echo ""

# Check if database exists
if [ ! -f "praisa_demo.db" ]; then
    echo "⚠️  Database not found. Running setup..."
    python scripts/setup_database.py
    echo ""
fi

# Start FastAPI server
echo "🚀 Starting FastAPI server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API docs will be available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
