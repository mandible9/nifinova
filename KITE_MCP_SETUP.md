
# Kite MCP Integration Setup

## Overview

This integration connects your NIFINOVA AI Trading Platform with Claude Desktop using Zerodha's Kite MCP protocol, enabling AI-powered trading through natural language commands.

## Setup Steps

### 1. Configure Kite Connect API

1. **Get Kite Connect API credentials:**
   - Visit [Zerodha Developer Console](https://developers.zerodha.com/)
   - Create a new app and get API key and secret
   - Generate access token using the authentication flow

2. **Set environment variables:**
   ```bash
   export ZERODHA_API_KEY="your_api_key_here"
   export ZERODHA_ACCESS_TOKEN="your_access_token_here"
   ```

### 2. Install Claude Desktop

1. **Download Claude Desktop** from Anthropic's website
2. **Locate the configuration file:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

### 3. Configure Claude Desktop

1. **Copy the MCP configuration:**
   ```bash
   cp claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json
   ```

2. **Update the configuration path:**
   - Edit the `claude_desktop_config.json` file
   - Update the path to point to your Repl's `kite_mcp_integration.py` file

3. **Add your API credentials to the env section**

### 4. Start the MCP Server

```bash
python kite_mcp_integration.py
```

### 5. Test in Claude Desktop

Once configured, you can use these commands in Claude Desktop:

**Portfolio Management:**
- "Show my current portfolio"
- "What are my today's positions?"
- "Get NIFTY quote"

**AI Trading:**
- "Generate high-confidence trading signals"
- "Analyze Nifty options chain"
- "Calculate risk for buying 50 NIFTY 19850 CE at ₹45"

**Order Management:**
- "Place order: BUY 50 NIFTY 19850 CE"
- "Show my order status"

## Available Tools

1. **get_portfolio** - View holdings and P&L
2. **get_positions** - Current day's trading positions
3. **get_quote** - Real-time quotes for any symbol
4. **place_order** - Place trading orders
5. **get_nifty_options_chain** - Complete options chain with AI analysis
6. **generate_ai_trading_signal** - AI-powered trading signals
7. **risk_analysis** - Position sizing and risk calculations

## Security Features

- All orders require confirmation
- Risk analysis for every trade
- Capital protection with position sizing
- Demo mode when API credentials not configured

## Integration Benefits

- **Natural Language Trading:** Place orders using plain English
- **AI-Powered Analysis:** Get intelligent market insights
- **Risk Management:** Automatic position sizing and risk calculations
- **Real-time Data:** Live market quotes and portfolio updates
- **Seamless Workflow:** Trade directly from Claude Desktop

## Troubleshooting

1. **MCP Server not starting:**
   - Check Python dependencies: `pip install mcp`
   - Verify file permissions

2. **Claude Desktop not connecting:**
   - Ensure config file path is correct
   - Restart Claude Desktop after configuration

3. **API errors:**
   - Verify Kite Connect credentials
   - Check API rate limits
   - Ensure market hours for live data

## Production Deployment

For production use on Replit:

1. **Use Replit Secrets** for API credentials
2. **Deploy as Reserved VM** for consistent uptime
3. **Configure webhook endpoints** for real-time updates
4. **Enable monitoring** for API health checks

Your NIFINOVA platform now has full Claude Desktop integration for AI-powered trading! 🚀
