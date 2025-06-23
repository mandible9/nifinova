# Nifty AI Trading Assistant

An AI-powered Nifty 50 options trading application with real-time signals and WhatsApp notifications.

## Features

- **AI Trading Signals**: Automated generation of buy/sell signals with confidence levels
- **Zerodha Integration**: Real-time market data and options chain
- **WhatsApp Notifications**: Instant alerts for strong buy signals (90%+ confidence)
- **Portfolio Tracking**: Monitor your positions and P&L
- **Options Chain**: Live options data with strike prices and volumes
- **User Management**: Add/remove WhatsApp numbers for notifications

## Prerequisites

- Node.js 18 or higher
- A Zerodha trading account (optional - app works with demo data)
- WhatsApp Business API access (optional - for notifications)

## Installation & Setup

### 1. Download and Extract

1. Download the project zip file
2. Extract to your preferred directory
3. Open terminal/command prompt in the project folder

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Setup (Optional)

Create a `.env` file in the root directory for Zerodha and WhatsApp integration:

```env
# Zerodha API Configuration
ZERODHA_API_KEY=your_api_key_here
ZERODHA_ACCESS_TOKEN=your_access_token_here

# WhatsApp Business API Configuration
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
```

### 4. Run the Application

```bash
npm run dev
```

The app will start on `http://localhost:5000`

## Zerodha Integration Guide

### Step 1: Create Zerodha Developer Account

1. Visit [Kite Connect](https://kite.trade/)
2. Sign up for a developer account
3. Create a new app to get your API key

### Step 2: Get API Credentials

1. **API Key**: Available in your Kite Connect dashboard
2. **Access Token**: Generate using the authentication flow

### Step 3: Authentication Flow

```javascript
// Example authentication URL
https://kite.trade/connect/login?api_key=YOUR_API_KEY&v=3
```

After login, you'll receive a request token. Exchange it for an access token:

```javascript
// Use Zerodha's KiteConnect library
const kc = new KiteConnect({
  api_key: "your_api_key"
});

// Generate access token
const response = await kc.generateSession("request_token", "api_secret");
const access_token = response.access_token;
```

### Step 4: Update Environment Variables

Add your credentials to the `.env` file:

```env
ZERODHA_API_KEY=your_actual_api_key
ZERODHA_ACCESS_TOKEN=your_actual_access_token
```

## WhatsApp Integration Guide

### Step 1: WhatsApp Business API Setup

1. Create a [Meta for Developers](https://developers.facebook.com/) account
2. Create a new app and add WhatsApp Business API
3. Get your access token and phone number ID

### Step 2: Configure Webhook (Optional)

For two-way communication, set up a webhook endpoint to receive messages.

### Step 3: Update Environment Variables

```env
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
```

## Usage

### 1. Login

- **Username**: `admin`
- **Password**: `admin`

### 2. Dashboard Overview

- View real-time Nifty 50 price and changes
- Monitor active AI signals
- Track success rates and portfolio performance

### 3. Managing WhatsApp Users

1. Navigate to the WhatsApp Management section
2. Add phone numbers in international format (+91XXXXXXXXXX)
3. Users will receive a welcome message
4. Strong buy signals (90%+ confidence) are automatically sent

### 4. AI Signals

- Signals are generated every 2 minutes
- Based on technical indicators (RSI, SMA, volume, volatility)
- High-confidence signals trigger WhatsApp notifications
- Each signal includes target price and stop loss

### 5. Options Chain

- View live options data for current week
- Call and Put options with LTP and volume
- ATM (At The Money) strikes are highlighted

## Demo Mode

The app works perfectly without API keys:

- **Market Data**: Uses realistic mock data
- **WhatsApp**: Logs messages to console instead of sending
- **Signals**: AI generates signals based on simulated market conditions

## Technical Architecture

### Frontend
- **React** with TypeScript
- **Tailwind CSS** for styling
- **Wouter** for routing
- **TanStack Query** for data fetching
- **Shadcn/ui** components

### Backend
- **Express.js** server
- **In-memory storage** for demo purposes
- **RESTful API** endpoints
- **Session-based authentication**

### AI Signal Generation
- Technical analysis using RSI, SMA, volume
- Market condition assessment
- Confidence scoring algorithm
- Automated WhatsApp notifications

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout  
- `GET /api/auth/me` - Get current user

### Market Data
- `GET /api/market/overview` - Dashboard overview
- `GET /api/market/nifty` - Nifty 50 quote
- `GET /api/market/options-chain` - Options chain data

### Trading Signals
- `GET /api/signals` - Get active signals

### WhatsApp Management
- `GET /api/whatsapp/users` - List WhatsApp users
- `POST /api/whatsapp/users` - Add WhatsApp user
- `DELETE /api/whatsapp/users/:phoneNumber` - Remove user

### Portfolio
- `GET /api/portfolio/positions` - Get positions
- `GET /api/portfolio/summary` - Portfolio summary

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port in `package.json` scripts
2. **API rate limits**: Zerodha has rate limiting - signals generate every 2 minutes
3. **WhatsApp verification**: Ensure phone numbers are verified on WhatsApp Business
4. **CORS issues**: App runs frontend and backend on same port to avoid CORS

### Logs

Check the console for detailed logs:
- AI signal generation status
- API request/response details
- WhatsApp message sending status

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement proper authentication in production
- Consider using database instead of in-memory storage for production

## License

This project is for educational and demo purposes. Please ensure compliance with Zerodha's terms of service and WhatsApp's business policies when using their APIs.

## Support

For technical issues:
1. Check the console logs for error details
2. Verify API credentials and rate limits
3. Ensure proper phone number formatting for WhatsApp
4. Test with demo mode first before integrating live APIs

---

**Disclaimer**: This is a demo application for educational purposes. Always trade responsibly and at your own risk. Past performance does not guarantee future results.