# Nifty AI Trading Assistant

A Python-based AI-powered trading application for Nifty 50 options with real-time data updates every 1 second.

## Features

- **Real-time AI Trading Signals**: Generates CALL/PUT signals every second
- **Live Market Data**: Nifty 50 prices updated continuously
- **Options Chain Display**: Real-time options data
- **WhatsApp Notifications**: Send strong buy signals to users
- **Portfolio Tracking**: Monitor trading performance
- **Web Dashboard**: Clean, responsive interface

## Quick Start

1. **Start the application**:
   ```bash
   python start_python_server.py
   ```

2. **Access the dashboard**:
   - URL: http://localhost:5000
   - Login: admin / admin

## API Integrations

### Zerodha Integration
Currently using mock data for development. To enable live trading:

1. Get API credentials from Zerodha Kite Connect
2. Set environment variables:
   ```bash
   export ZERODHA_API_KEY="your_api_key"
   export ZERODHA_ACCESS_TOKEN="your_access_token"
   ```

### WhatsApp Integration
Currently using mock data for development. To enable notifications:

1. Get WhatsApp Business API credentials
2. Set environment variables:
   ```bash
   export WHATSAPP_ACCESS_TOKEN="your_access_token"
   export WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id"
   ```

## Files Structure

```
├── app.py                    # Main Flask application
├── start_python_server.py    # Application launcher
├── templates/
│   ├── base.html            # Base template
│   ├── login.html           # Login page
│   └── dashboard.html       # Main dashboard
└── README.md                # This file
```

## Dependencies

- Flask
- Flask-SocketIO
- Requests
- Python-dotenv

## Data Updates

The application provides real-time data updates:
- Market data: Every 1 second
- AI signals: Generated continuously
- Options chain: Updated in real-time
- WebSocket connections: Live dashboard updates