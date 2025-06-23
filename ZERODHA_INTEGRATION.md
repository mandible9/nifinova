# Zerodha Integration Guide

## Overview
This guide explains how to connect your Zerodha trading account to get real market data and enable live options trading signals.

## Prerequisites
- Active Zerodha trading account
- Kite Connect subscription (₹2000/month + GST)
- Basic understanding of API authentication

## Step 1: Subscribe to Kite Connect

1. Visit [Kite Connect](https://kite.trade/)
2. Login with your Zerodha credentials
3. Subscribe to Kite Connect API service
4. Pay the subscription fee (₹2000/month + GST)

## Step 2: Create Application

1. Go to Kite Connect dashboard
2. Click "Create new app"
3. Fill in application details:
   - **App name**: Nifty AI Trading Assistant
   - **App type**: Connect
   - **Redirect URL**: http://localhost:5000/auth/callback
4. Save the application
5. Note down your **API Key** and **API Secret**

## Step 3: Generate Access Token

### Method 1: Manual Authentication (Recommended for testing)

1. Create login URL with your API key:
```
https://kite.trade/connect/login?api_key=YOUR_API_KEY&v=3
```

2. Open this URL in browser and login
3. After successful login, you'll be redirected to your callback URL with a `request_token`
4. Extract the `request_token` from the URL

### Method 2: Programmatic Authentication

Create a simple script to generate access token:

```javascript
const KiteConnect = require("kiteconnect").KiteConnect;

const kc = new KiteConnect({
  api_key: "YOUR_API_KEY"
});

// After getting request_token from login flow
const session = await kc.generateSession("REQUEST_TOKEN", "API_SECRET");
console.log("Access Token:", session.access_token);
```

## Step 4: Configure Environment

1. Copy `.env.example` to `.env`
2. Add your Zerodha credentials:

```env
ZERODHA_API_KEY=your_api_key_here
ZERODHA_ACCESS_TOKEN=your_access_token_here
```

## Step 5: Verify Integration

1. Restart the application:
```bash
npm run dev
```

2. Check the console logs for successful connection
3. Monitor the dashboard for real market data

## API Endpoints Used

### Market Data
- **Quote**: `/quote?i=NSE:NIFTY 50` - Get Nifty 50 current price
- **Options Chain**: `/quote?i=NFO:NIFTY...` - Get options prices

### Rate Limits
- **3 requests per second**
- **1000 requests per day**
- **200 concurrent connections**

## Data Available

### Real-time Data
- Nifty 50 current price and changes
- Options chain with LTP (Last Traded Price)
- Volume and open interest
- Bid/ask prices

### Historical Data
- OHLC (Open, High, Low, Close) data
- Volume information
- Time series data for backtesting

## Security Considerations

### Access Token Security
- Access tokens expire after login session
- Store tokens securely, never in version control
- Regenerate tokens if compromised

### API Key Protection
- Never expose API keys in client-side code
- Use environment variables only
- Monitor API usage regularly

## Troubleshooting

### Common Issues

**1. Authentication Errors**
```
Error: Incorrect API credentials
```
- Verify API key and access token
- Check if tokens have expired
- Ensure proper URL encoding

**2. Rate Limit Exceeded**
```
Error: Too many requests
```
- Implement request throttling
- Current app respects 3 req/sec limit
- Monitor daily usage

**3. Instrument Token Issues**
```
Error: Invalid instrument
```
- Use correct instrument tokens
- Verify option symbols format
- Check expiry dates

### Debug Mode

Enable detailed logging by adding to `.env`:
```env
DEBUG=zerodha:*
```

## Testing Without Live Account

The application includes comprehensive mock data that simulates real market conditions:
- Realistic price movements
- Volume fluctuations
- Options pricing models
- Signal generation algorithms

This allows full testing without API costs.

## Production Deployment

### Token Management
- Implement automatic token refresh
- Use secure storage for credentials
- Monitor token expiry

### Error Handling
- Graceful fallback to demo data
- Retry mechanisms for API failures
- Alert systems for connection issues

### Monitoring
- Track API usage and costs
- Monitor signal accuracy
- Log all trading decisions

## Cost Optimization

### Reduce API Calls
- Cache frequently requested data
- Use websockets for real-time updates
- Batch multiple requests

### Subscription Management
- Monitor monthly usage
- Optimize request patterns
- Consider data provider alternatives

## Legal and Compliance

### Terms of Service
- Comply with Zerodha's API terms
- Respect rate limiting requirements
- Use data only for personal trading

### Risk Management
- This is an educational tool
- Not financial advice
- Trade at your own risk
- Implement proper risk controls

---

**Need Help?** Check the console logs for detailed error messages and API response details.