# Quick Setup Guide - Nifty AI Trading Assistant

## 🚀 Quick Start (5 minutes)

### 1. Download & Extract
- Extract the project zip to your preferred folder
- Open terminal/command prompt in that folder

### 2. Install & Run
```bash
npm install
npm run dev
```

### 3. Access Application
- Open browser: `http://localhost:5000`
- Login: Username `admin`, Password `admin`

**The app works immediately with demo data - no setup required!**

---

## 🔗 Zerodha Integration (Optional)

### Prerequisites
- Active Zerodha trading account
- Kite Connect subscription (₹2000/month)

### Step 1: Get API Access
1. Visit [Kite Connect](https://kite.trade/)
2. Login with your Zerodha credentials
3. Subscribe to Kite Connect API
4. Create a new app to get your API Key

### Step 2: Generate Access Token
1. Use the login URL with your API key:
```
https://kite.trade/connect/login?api_key=YOUR_API_KEY&v=3
```

2. After login, you'll get a `request_token` in the URL
3. Exchange it for an access token using Zerodha's libraries or direct API call

### Step 3: Environment Setup
Create a `.env` file in the project root:
```env
ZERODHA_API_KEY=your_api_key_here
ZERODHA_ACCESS_TOKEN=your_access_token_here
```

### Step 4: Restart Application
```bash
npm run dev
```

---

## 📱 WhatsApp Integration (Optional)

### Option 1: WhatsApp Business API (Recommended)
1. Create [Meta for Developers](https://developers.facebook.com/) account
2. Create new app → Add WhatsApp Business API
3. Get your Phone Number ID and Access Token
4. Add to `.env` file:
```env
WHATSAPP_ACCESS_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id_here
```

### Option 2: Third-Party Services
- **Twilio**: Easy setup, pay-per-message
- **MessageBird**: Global coverage
- **WhatsApp Business Platform**: Direct integration

---

## 📊 How It Works

### AI Signal Generation
- Analyzes technical indicators every 2 minutes
- RSI, Moving Averages, Volume, Volatility
- Generates confidence scores (60-98%)
- High-confidence signals (90%+) trigger WhatsApp alerts

### Signal Types
- **CALL**: Bullish signals for upward movement
- **PUT**: Bearish signals for downward movement
- Each includes target price and stop loss

### WhatsApp Notifications
Users receive formatted messages like:
```
🚨 STRONG BUY SIGNAL 🚨

📈 CALL Signal
🎯 Strike: 19850
💪 Confidence: 92%

📊 Trade Details:
• Target: ₹45.50
• Stop Loss: ₹18.20

💡 AI Analysis:
Strong bullish momentum detected, RSI oversold recovery pattern

⚠️ Risk Disclaimer: Trading involves risk.
```

---

## 🔧 Troubleshooting

### Port Already in Use
Change port in `package.json`:
```json
"scripts": {
  "dev": "NODE_ENV=development tsx server/index.ts --port 3000"
}
```

### API Rate Limits
- Zerodha: 3 requests/second, 1000/day
- Signals generate every 2 minutes to respect limits

### WhatsApp Issues
- Verify phone numbers are WhatsApp verified
- Use international format: +91XXXXXXXXXX
- Check console logs for sending status

### Memory Usage
For production, consider:
- Database instead of in-memory storage
- Redis for session management
- Process clustering for scalability

---

## 🔒 Security Best Practices

### API Keys
- Never commit `.env` files to version control
- Rotate API keys regularly
- Monitor API usage and billing

### Production Deployment
- Enable HTTPS
- Use secure session secrets
- Implement rate limiting
- Add proper error handling

---

## 📈 Features Overview

### Dashboard
- Real-time Nifty 50 price updates
- AI signal generation status
- Success rate tracking
- WhatsApp user management

### Options Chain
- Live call/put prices and volumes
- ATM (At The Money) highlighting
- Multiple expiry dates
- Real-time updates

### Portfolio Tracking
- Position monitoring
- P&L calculations
- Performance metrics
- Trade history

---

## 🆘 Support

### Common Issues
1. **Login fails**: Check username/password (admin/admin)
2. **No signals**: Wait 2 minutes for AI generation cycle
3. **WhatsApp not sending**: Verify credentials and phone format
4. **API errors**: Check rate limits and credentials

### Debug Mode
Check browser console and terminal for detailed logs:
- API request/response details
- Signal generation status
- WhatsApp sending confirmation

### Demo Mode Benefits
- No API costs or setup required
- Realistic market simulation
- Full feature testing
- Safe learning environment

---

**Ready to start trading? The app works immediately with demo data. Add real API keys when you're ready for live trading!**