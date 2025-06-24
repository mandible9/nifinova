
# MCP Server for Zerodha Trading with AI

This MCP (Model Context Protocol) server provides AI-powered trading tools and prompts for Zerodha integration.

## Features

### 🛠️ Available Tools

1. **get_market_data** - Real-time Nifty 50 market data
2. **get_options_chain** - Complete options chain with strike prices and premiums
3. **generate_ai_signal** - AI-generated trading signals with confidence scores
4. **analyze_trade_opportunity** - Comprehensive analysis of specific trades
5. **risk_management_analysis** - Position sizing and risk calculations
6. **market_sentiment_analysis** - Multi-factor sentiment analysis

### 💭 Available Prompts

1. **trading_strategy** - Generate comprehensive trading strategies
2. **technical_analysis** - Detailed technical analysis of Nifty 50
3. **options_strategy** - Options strategies based on market outlook

## Installation

1. **Install dependencies:**
   ```bash
   python install_mcp.py
   ```

2. **Start the MCP server:**
   ```bash
   python mcp_server.py
   ```

3. **Test with example client:**
   ```bash
   python mcp_client_example.py
   ```

## Usage Examples

### Getting Market Data
```python
result = await session.call_tool("get_market_data", {})
```

### Generating AI Signals
```python
result = await session.call_tool("generate_ai_signal", {
    "confidence_threshold": 85,
    "signal_type": "CALL"
})
```

### Analyzing Trade Opportunities
```python
result = await session.call_tool("analyze_trade_opportunity", {
    "strike_price": 19850,
    "option_type": "CALL",
    "capital": 25000
})
```

### Risk Management Analysis
```python
result = await session.call_tool("risk_management_analysis", {
    "entry_price": 45.50,
    "target_price": 68.00,
    "stop_loss": 34.00,
    "capital": 50000,
    "risk_percentage": 2
})
```

## Integration with Claude Desktop

To use this MCP server with Claude Desktop, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zerodha-trading": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"],
      "env": {
        "ZERODHA_API_KEY": "your_api_key",
        "ZERODHA_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

## API Integration

The server uses your existing Zerodha and AI services:
- **ZerodhaService** for market data and options chain
- **AISignalsService** for signal generation
- Mock data is used when API credentials are not available

## Features

- **Real-time Analysis**: Every tool provides up-to-date market analysis
- **Risk Management**: Built-in position sizing and risk calculations
- **AI Integration**: Leverages your existing AI signal generation
- **Comprehensive Coverage**: From basic market data to complex strategy analysis
- **User-Friendly**: Clear, formatted responses with actionable insights

## Security

- Environment variables for API keys
- Error handling for API failures
- Mock data fallback for development
- No sensitive data logged

This MCP server transforms your trading application into a powerful AI assistant that can be used with any MCP-compatible client!
