@echo off
TITLE TravelSync - AI Travel Planner Launcher
echo ========================================================
echo   Starting TravelSync AI Multi-Agent System
echo ========================================================

echo 1. Starting Python AI Service (Port 8000)...
start "TravelSync AI Service (Port 8000)" cmd /k "cd ai-service && python main.py"

timeout /t 3 /nobreak >nul

echo 2. Starting Node.js API Gateway (Port 5000)...
start "TravelSync Backend Gateway (Port 5000)" cmd /k "cd backend && npm start"

timeout /t 2 /nobreak >nul

echo 3. Starting React Frontend (Port 3000)...
start "TravelSync Frontend (Port 3000)" cmd /k "cd frontend && npm run dev"

echo.
echo All services launched!
echo Web Application: http://localhost:3000
echo API Gateway:     http://localhost:5000
echo Python AI Docs:  http://127.0.0.1:8000/docs
echo ========================================================
