# Nifty AI Trading Assistant

## Overview

This is a Python-based AI-powered trading application for Nifty 50 options trading with real-time data processing and WebSocket integration. The application provides live trading signals, market data analysis, and portfolio tracking with a modern web interface.

## System Architecture

### Frontend Architecture
- **Web Interface**: Flask-based web application with HTML templates
- **Real-time Updates**: WebSocket communication using Flask-SocketIO for live data streaming
- **Responsive Design**: Tailwind CSS for modern, mobile-first UI
- **Interactive Dashboard**: Real-time market data visualization and trading signals

### Backend Architecture
- **Core Framework**: Flask web framework with Python 3.11+
- **Real-time Processing**: Background threads for continuous market data processing
- **AI Signal Generation**: Integrated AI service for trading signal analysis
- **WebSocket Server**: Flask-SocketIO for real-time client-server communication
- **Session Management**: Flask sessions for user authentication

### Integration Layer
- **Market Data**: Zerodha Kite Connect API integration (with mock data fallback)
- **AI Services**: Claude AI API for trading signal generation
- **Notifications**: WhatsApp Business API for signal alerts
- **MCP Server**: Model Context Protocol server for AI tool integration

## Key Components

### Core Services
1. **ZerodhaService**: Market data retrieval and options chain processing
2. **AISignalsService**: AI-powered trading signal generation with confidence scoring
3. **TradingSignal**: Data model for trading recommendations with risk analysis
4. **MarketData**: Real-time Nifty 50 price and volume data
5. **OptionsData**: Live options chain with strike prices and premiums

### Authentication System
- Simple username/password authentication
- Session-based login management
- Default credentials: pkrsolution/prabhanjan2025

### Real-time Features
- Live market data updates every 1 second
- Continuous AI signal generation
- WebSocket-based real-time dashboard updates
- Automatic market status detection

## Data Flow

1. **Market Data Collection**: ZerodhaService fetches live market data or uses mock data
2. **AI Processing**: AISignalsService analyzes market conditions and generates trading signals
3. **Signal Broadcasting**: WebSocket server broadcasts signals to connected clients
4. **Client Updates**: Dashboard receives real-time updates and displays current market state
5. **Notification Pipeline**: High-confidence signals trigger WhatsApp notifications

## External Dependencies

### Required APIs
- **Zerodha Kite Connect**: For live market data (optional, falls back to mock data)
- **Claude AI**: For trading signal generation and market analysis
- **WhatsApp Business API**: For signal notifications (optional)

### Python Dependencies
- Flask & Flask-SocketIO for web framework and real-time communication
- Anthropic for Claude AI integration
- Requests for HTTP API calls
- PyTZ for timezone handling
- MCP for Model Context Protocol integration

### Node.js Dependencies (Development)
- Vite for build tooling
- Express for server management
- TypeScript for type safety
- Various UI libraries (@radix-ui components)

## Deployment Strategy

### Development Environment
- **Local Server**: Python Flask development server on port 5000
- **Auto-reload**: Development mode with live code reloading
- **Mock Data**: Simulated market data for testing without API keys

### Production Environment
- **Build Process**: Vite build for frontend assets, ESBuild for backend
- **Deployment Target**: Replit autoscale deployment
- **Environment Variables**: API keys and configuration via .env files
- **Database**: PostgreSQL for production data persistence (optional)

### Startup Process
1. Initialize Flask application with SocketIO
2. Start background AI signal generation thread
3. Launch WebSocket server for real-time communication
4. Serve web interface on configured port

## Changelog

- June 25, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.