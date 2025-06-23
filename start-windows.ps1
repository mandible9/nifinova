Write-Host "Starting Nifty AI Trading Assistant..." -ForegroundColor Green
Write-Host ""
Write-Host "Application will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Login with: Username = admin, Password = admin" -ForegroundColor Yellow
Write-Host ""

# Set environment variable for this session
$env:NODE_ENV = "development"

# Start the application
Write-Host "Starting server..." -ForegroundColor Yellow

try {
    # Start the server in a new process
    $serverJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        $env:NODE_ENV = "development"
        tsx server/index.ts
    }
    
    # Wait a few seconds for server to start
    Write-Host "Waiting for server to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Open the browser
    Write-Host "Opening browser..." -ForegroundColor Green
    Start-Process "http://localhost:5000"
    
    # Show server status
    Write-Host ""
    Write-Host "Server is running! Browser should open automatically." -ForegroundColor Green
    Write-Host "If browser doesn't open, visit: http://localhost:5000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to stop the server..." -ForegroundColor Yellow
    
    # Wait for user input to stop
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Stop the server
    Stop-Job $serverJob
    Remove-Job $serverJob
    Write-Host "Server stopped." -ForegroundColor Red
}
catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host "Make sure you have run 'npm install' first" -ForegroundColor Yellow
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}