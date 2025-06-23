Write-Host "Starting Nifty AI Trading Assistant..." -ForegroundColor Green
Write-Host ""

# Set environment variable for this session
$env:NODE_ENV = "development"

# Start the application
Write-Host "Environment: Development" -ForegroundColor Yellow
Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host ""

try {
    tsx server/index.ts
}
catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host "Make sure you have run 'npm install' first" -ForegroundColor Yellow
    pause
}