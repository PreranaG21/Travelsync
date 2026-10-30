# TravelSync Multi-Agent System - Windows PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting TravelSync AI Multi-Agent System (Windows)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "1. Starting Python AI Service (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\ai-service'; python main.py"

Start-Sleep -Seconds 3

Write-Host "2. Starting Node.js API Gateway (Port 5000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\backend'; npm run dev"

Start-Sleep -Seconds 2

Write-Host "3. Starting React Frontend (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\frontend'; npm run dev"

Write-Host ""
Write-Host "All 3 services launched successfully!" -ForegroundColor Green
Write-Host "• Frontend Web App:  http://localhost:3000" -ForegroundColor Green
Write-Host "• Backend Gateway:   http://localhost:5000" -ForegroundColor Green
Write-Host "• Python AI Docs:    http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "• Health Check:      http://localhost:5000/api/health" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
