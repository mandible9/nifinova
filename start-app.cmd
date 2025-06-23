@echo off
title Nifty AI Trading Assistant
color 0A

echo.
echo ===============================================
echo    NIFTY AI TRADING ASSISTANT
echo ===============================================
echo.
echo Starting application...
echo URL: http://localhost:5000
echo Login: admin / admin
echo.

REM Set environment and start server
set NODE_ENV=development
echo Starting server in background...
start /B tsx server/index.ts

REM Wait for server to initialize
echo Waiting for server to start...
ping localhost -n 6 > nul

REM Open browser automatically
echo Opening browser...
start http://localhost:5000

echo.
echo ===============================================
echo Server is now running!
echo Browser should open automatically.
echo Close this window to stop the server.
echo ===============================================
echo.

REM Keep window open - server runs until window is closed
pause > nul