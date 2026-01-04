@echo off
REM PRAISA Demo Startup Script for Windows
REM 
REM This script starts both Backend and Frontend for the demo.
REM It opens separate windows for each process.

echo =========================================
echo PRAISA - Starting Demo Environment
echo =========================================
echo.

REM 1. Start Backend
echo [1/2] Launching Backend (FastAPI)...
start "PRAISA Backend" cmd /k "venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 2. Start Frontend
echo [2/2] Launching Frontend (Vite)...
cd frontend
start "PRAISA Frontend" cmd /k "npm run dev"
cd ..

echo.
echo =========================================
echo ✅ Services Started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo =========================================
echo.
echo Don't close the new windows!
pause
