# Launch Instructions - Windows Users

## Easiest Method (Recommended)

**Double-click any of these files:**
- `start-app.cmd` - Best option with formatted output
- `start-windows.bat` - Simple batch file
- `start-windows.ps1` - PowerShell version

The application will:
1. Start the server automatically
2. Wait 5 seconds for initialization  
3. Open your default browser to http://localhost:5000
4. Show login page (admin/admin)

## What You'll See

1. **Command window opens** showing startup progress
2. **Browser launches** automatically after 5 seconds
3. **Login page** appears - use `admin` for both username and password
4. **Trading dashboard** loads with live AI signals

## Stopping the Application

- Close the command window, or
- Press Ctrl+C in the command window

## Manual Alternative

If double-clicking doesn't work, open Command Prompt in the project folder:

```cmd
set NODE_ENV=development
npx tsx server/index.ts
```

Then manually visit: http://localhost:5000

## First Time Setup

Before running for the first time:
```cmd
npm install
```

## Features Available Immediately

- Real-time AI trading signal generation (every 2 minutes)
- Live options chain data
- WhatsApp user management
- Portfolio tracking
- Market overview dashboard

All features work with realistic demo data - no API setup required for testing.