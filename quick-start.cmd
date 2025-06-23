@echo off
title Nifty AI Trading Assistant - Quick Start
color 0A

echo.
echo ===============================================
echo    NIFTY AI TRADING ASSISTANT
echo ===============================================
echo.
echo Checking dependencies...

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    echo.
)

echo Starting application...
echo URL: http://localhost:5000
echo Login: admin / admin
echo.

REM Set environment and start server
set NODE_ENV=development

REM Start server directly (not in background to see output)
echo Server starting...
echo.
npx tsx server/index.ts

pause