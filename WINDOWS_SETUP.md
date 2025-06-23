# Windows Setup Guide - Nifty AI Trading Assistant

## Quick Start for Windows Users

### Option 1: Using Batch File (Recommended)
1. Double-click `start-windows.bat`
2. The application will start automatically
3. Open browser: `http://localhost:5000`
4. Login: Username `admin`, Password `admin`

### Option 2: Using PowerShell
1. Right-click `start-windows.ps1` → "Run with PowerShell"
2. If prompted about execution policy, type `Y` and press Enter
3. Open browser: `http://localhost:5000`
4. Login: Username `admin`, Password `admin`

### Option 3: Manual Commands
Open Command Prompt or PowerShell in the project folder:

**Command Prompt:**
```cmd
set NODE_ENV=development
npx tsx server/index.ts
```

**PowerShell:**
```powershell
$env:NODE_ENV="development"
npx tsx server/index.ts
```

## First Time Setup

1. **Extract the project** to your desired folder
2. **Open Command Prompt or PowerShell** in that folder
3. **Install dependencies:**
   ```cmd
   npm install
   ```
4. **Start the application** using any method above

## Troubleshooting

### Common Issues

**"tsx is not recognized"**
```cmd
npm install -g tsx
```

**"Permission denied" in PowerShell**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port 5000 already in use**
- Close other applications using port 5000
- Or modify the port in `server/index.ts`

### Alternative Ports
If port 5000 is busy, try these commands:

**Command Prompt:**
```cmd
set NODE_ENV=development
set PORT=3000
npx tsx server/index.ts
```

**PowerShell:**
```powershell
$env:NODE_ENV="development"
$env:PORT="3000"
npx tsx server/index.ts
```

## Features Overview

Once running, you'll have access to:
- Real-time AI trading signals
- WhatsApp notification management
- Live options chain data
- Portfolio tracking
- Market overview dashboard

The application works immediately with realistic demo data. No API keys required for testing.

## Next Steps

1. **Test the application** with demo data
2. **Add WhatsApp numbers** for notifications
3. **Review AI signals** as they generate
4. **Integrate Zerodha API** for live data (optional)

For Zerodha integration, see `ZERODHA_INTEGRATION.md`.