@echo off
echo Starting Nifty AI Trading Assistant...
echo.
echo Application will be available at: http://localhost:5000
echo Login with: Username = admin, Password = admin
echo.
echo Starting server...

set NODE_ENV=development

REM Start the server in background and open browser
start "" npx tsx server/index.ts

REM Wait a few seconds for server to start, then open browser
timeout /t 5 /nobreak >nul
start "" "http://localhost:5000"

REM Keep the command window open
echo.
echo Server is running. Close this window to stop the application.
echo Press Ctrl+C to stop the server.
pause