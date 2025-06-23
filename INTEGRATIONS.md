# API Integrations Setup

## Zerodha Kite Connect Integration

The application currently uses simulated market data. To connect to live Zerodha data:

### Steps to Enable:
1. **Register for Kite Connect API**:
   - Visit https://kite.trade/
   - Sign up for API access
   - Get your API key and secret

2. **Generate Access Token**:
   - Use Zerodha's authentication flow
   - Generate daily access token

3. **Set Environment Variables**:
   ```bash
   export ZERODHA_API_KEY="your_api_key_here"
   export ZERODHA_ACCESS_TOKEN="your_access_token_here"
   ```

4. **Restart the application** - it will automatically detect and use live data

### What You'll Get:
- Real Nifty 50 prices
- Live options chain data
- Actual market volumes
- Historical data access

---

## WhatsApp Business API Integration

The application includes WhatsApp notification functionality. To enable:

### Steps to Enable:
1. **Get WhatsApp Business API Access**:
   - Register at https://developers.facebook.com/
   - Set up WhatsApp Business API
   - Get phone number ID and access token

2. **Set Environment Variables**:
   ```bash
   export WHATSAPP_ACCESS_TOKEN="your_access_token_here"
   export WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id_here"
   ```

3. **Restart the application** - notifications will start working

### What You'll Get:
- Automatic WhatsApp messages for high-confidence signals (90%+)
- User management through dashboard
- Formatted trading alerts with targets and stop losses

---

## Current Status

**Without API Keys**: Application runs with realistic simulated data
**With API Keys**: Application connects to live market data and sends real notifications

Both integrations work seamlessly - just add the environment variables when you're ready to go live.