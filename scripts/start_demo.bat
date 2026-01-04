@echo off
REM PRAISA Demo Startup Script for Windows
REM 
REM This script starts the PRAISA backend server for demo purposes.
REM Usage: scripts\start_demo.bat

echo =========================================
echo PRAISA - Starting Demo Server
echo =========================================
echo.

REM Check if database exists
if not exist "praisa_demo.db" (
    echo [WARNING] Database not found. Running setup...
    python scripts\setup_database.py
    echo.
)

REM Start FastAPI server
echo [INFO] Starting FastAPI server...
echo [INFO] API will be available at: http://localhost:8000
echo [INFO] API docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
