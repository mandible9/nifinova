
#!/usr/bin/env python3

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """Example client to interact with the Zerodha Trading MCP server"""
    
    # Start the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("🚀 Connected to Zerodha Trading MCP Server")
            print("=" * 50)
            
            # List available tools
            tools = await session.list_tools()
            print(f"📋 Available Tools ({len(tools.tools)}):")
            for tool in tools.tools:
                print(f"  • {tool.name}: {tool.description}")
            print()
            
            # List available prompts
            prompts = await session.list_prompts()
            print(f"💭 Available Prompts ({len(prompts.prompts)}):")
            for prompt in prompts.prompts:
                print(f"  • {prompt.name}: {prompt.description}")
            print()
            
            # Example 1: Get market data
            print("📊 Getting market data...")
            market_result = await session.call_tool("get_market_data", {})
            print(market_result.content[0].text)
            print()
            
            # Example 2: Generate AI signal
            print("🤖 Generating AI trading signal...")
            signal_result = await session.call_tool("generate_ai_signal", {
                "confidence_threshold": 80,
                "signal_type": "BOTH"
            })
            print(signal_result.content[0].text)
            print()
            
            # Example 3: Get options chain
            print("⛓️ Getting options chain...")
            options_result = await session.call_tool("get_options_chain", {})
            print(options_result.content[0].text[:500] + "...")  # Truncated for display
            print()
            
            # Example 4: Market sentiment analysis
            print("🎯 Analyzing market sentiment...")
            sentiment_result = await session.call_tool("market_sentiment_analysis", {
                "timeframe": "15min"
            })
            print(sentiment_result.content[0].text)
            print()
            
            # Example 5: Trading strategy prompt
            print("📈 Getting trading strategy...")
            strategy_prompt = await session.get_prompt("trading_strategy", {
                "market_outlook": "bullish",
                "risk_tolerance": "moderate", 
                "capital": "50000"
            })
            print(f"Strategy Prompt: {strategy_prompt.messages[0].content.text[:300]}...")
            print()
            
            print("✅ MCP Server test completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
