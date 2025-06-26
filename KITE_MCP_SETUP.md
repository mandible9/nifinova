
# Kite MCP Integration Setup

## Overview

This integration connects your NIFINOVA AI Trading Platform with Claude Desktop using Zerodha's official Kite MCP server, enabling AI-powered trading through natural language commands.

## Setup Steps

### 1. Authenticate with Kite Connect

1. **Login to Kite Connect:**
   - Use the provided authentication URL to login
   - Complete the OAuth flow to get your session token

2. **Authentication URL:**
   ```
   https://kite.zerodha.com/connect/login?api_key=kitemcp&v=3&redirect_params=session_id%3D0e712d6a-8155-4d21-9e53-5de289da5f60%7C1750955119.4P7yot0mscNAk8GWKIe7LghteVcRQ38sD1BR7UBU7mc%3D
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

2. **The configuration uses Zerodha's official MCP server:**
   ```json
   {
     "mcpServers": {
       "kite": {
         "command": "npx",
         "args": ["mcp-remote", "https://mcp.kite.trade/sse"]
       }
     }
   }
   ```

### 4. Available Commands

Once configured, you can use these commands in Claude Desktop:
- Get portfolio information
- Check positions
- Get real-time quotes
- Place orders (with confirmation)
- Analyze options chains
- Generate trading signals

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
