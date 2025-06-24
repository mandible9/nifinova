
#!/usr/bin/env python3

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    Prompt,
    PromptMessage,
    Role,
)
import mcp.types as types

# Import existing components from your app
from app import ZerodhaService, AISignalsService, TradingSignal, MarketData, OptionsData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zerodha-trading-mcp")

@dataclass
class TradeRecommendation:
    signal: TradingSignal
    risk_analysis: Dict[str, Any]
    entry_strategy: str
    exit_strategy: str
    position_size: float
    max_loss: float

class ZerodhaTradingMCP:
    def __init__(self):
        self.zerodha_service = ZerodhaService()
        self.ai_service = AISignalsService()
        self.server = Server("zerodha-trading-ai")
        
        # Setup MCP handlers
        self.setup_tools()
        self.setup_prompts()

    def setup_tools(self):
        """Setup MCP tools for trading operations"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_market_data",
                        description="Get real-time Nifty 50 market data including price, volume, and change",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Market symbol (default: NIFTY50)",
                                    "default": "NIFTY50"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="get_options_chain",
                        description="Get options chain data for Nifty 50 with strike prices, premiums, and volumes",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "expiry": {
                                    "type": "string",
                                    "description": "Expiry date (YYYY-MM-DD format, optional)",
                                    "default": "current_week"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="generate_ai_signal",
                        description="Generate AI-powered trading signal with technical analysis",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "confidence_threshold": {
                                    "type": "number",
                                    "description": "Minimum confidence level (60-95)",
                                    "default": 75
                                },
                                "signal_type": {
                                    "type": "string",
                                    "enum": ["CALL", "PUT", "BOTH"],
                                    "description": "Type of signal to generate",
                                    "default": "BOTH"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="analyze_trade_opportunity",
                        description="Comprehensive AI analysis of a specific trading opportunity",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "strike_price": {
                                    "type": "number",
                                    "description": "Strike price to analyze"
                                },
                                "option_type": {
                                    "type": "string",
                                    "enum": ["CALL", "PUT"],
                                    "description": "Option type"
                                },
                                "capital": {
                                    "type": "number",
                                    "description": "Available capital for trade",
                                    "default": 10000
                                }
                            },
                            "required": ["strike_price", "option_type"]
                        }
                    ),
                    Tool(
                        name="risk_management_analysis",
                        description="Calculate risk metrics and position sizing for a trade",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "entry_price": {
                                    "type": "number",
                                    "description": "Entry price for the option"
                                },
                                "target_price": {
                                    "type": "number",
                                    "description": "Target price"
                                },
                                "stop_loss": {
                                    "type": "number",
                                    "description": "Stop loss price"
                                },
                                "capital": {
                                    "type": "number",
                                    "description": "Total capital available"
                                },
                                "risk_percentage": {
                                    "type": "number",
                                    "description": "Maximum risk as percentage of capital",
                                    "default": 2
                                }
                            },
                            "required": ["entry_price", "target_price", "stop_loss", "capital"]
                        }
                    ),
                    Tool(
                        name="market_sentiment_analysis",
                        description="Analyze current market sentiment using multiple indicators",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "timeframe": {
                                    "type": "string",
                                    "enum": ["1min", "5min", "15min", "1hour", "1day"],
                                    "description": "Analysis timeframe",
                                    "default": "15min"
                                }
                            }
                        }
                    )
                ]
            )

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
            try:
                if name == "get_market_data":
                    return await self._get_market_data(arguments)
                elif name == "get_options_chain":
                    return await self._get_options_chain(arguments)
                elif name == "generate_ai_signal":
                    return await self._generate_ai_signal(arguments)
                elif name == "analyze_trade_opportunity":
                    return await self._analyze_trade_opportunity(arguments)
                elif name == "risk_management_analysis":
                    return await self._risk_management_analysis(arguments)
                elif name == "market_sentiment_analysis":
                    return await self._market_sentiment_analysis(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )

    def setup_prompts(self):
        """Setup MCP prompts for trading scenarios"""
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> ListPromptsResult:
            return ListPromptsResult(
                prompts=[
                    Prompt(
                        name="trading_strategy",
                        description="Generate a comprehensive trading strategy based on market conditions",
                        arguments=[
                            {
                                "name": "market_outlook",
                                "description": "Current market outlook (bullish/bearish/sideways)",
                                "required": True
                            },
                            {
                                "name": "risk_tolerance",
                                "description": "Risk tolerance level (conservative/moderate/aggressive)",
                                "required": True
                            },
                            {
                                "name": "capital",
                                "description": "Available trading capital",
                                "required": True
                            }
                        ]
                    ),
                    Prompt(
                        name="technical_analysis",
                        description": "Perform detailed technical analysis on Nifty 50",
                        arguments=[
                            {
                                "name": "timeframe",
                                "description": "Analysis timeframe",
                                "required": False
                            }
                        ]
                    ),
                    Prompt(
                        name="options_strategy",
                        description="Suggest options trading strategies based on market conditions",
                        arguments=[
                            {
                                "name": "market_direction",
                                "description": "Expected market direction",
                                "required": True
                            },
                            {
                                "name": "volatility_expectation",
                                "description": "Expected volatility (high/medium/low)",
                                "required": True
                            }
                        ]
                    )
                ]
            )

        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict) -> GetPromptResult:
            if name == "trading_strategy":
                return await self._get_trading_strategy_prompt(arguments)
            elif name == "technical_analysis":
                return await self._get_technical_analysis_prompt(arguments)
            elif name == "options_strategy":
                return await self._get_options_strategy_prompt(arguments)
            else:
                raise ValueError(f"Unknown prompt: {name}")

    # Tool implementation methods
    async def _get_market_data(self, args: dict) -> CallToolResult:
        """Get current market data"""
        try:
            quote = self.zerodha_service.get_nifty_quote()
            
            market_data = {
                "symbol": "NIFTY50",
                "current_price": quote["last_price"],
                "change": quote["change"],
                "change_percent": quote["net_change"],
                "volume": quote["volume"],
                "timestamp": datetime.now().isoformat(),
                "status": "ACTIVE" if abs(quote["change"]) > 0 else "INACTIVE"
            }
            
            analysis = f"""
📊 **NIFTY 50 Market Data**

**Current Price:** ₹{market_data['current_price']:.2f}
**Change:** {market_data['change']:+.2f} ({market_data['change_percent']:+.2f}%)
**Volume:** {market_data['volume']:,}
**Status:** {market_data['status']}

**Quick Analysis:**
- Market is {'bullish' if market_data['change'] > 0 else 'bearish' if market_data['change'] < 0 else 'sideways'}
- Volume is {'high' if market_data['volume'] > 1000000 else 'normal'}
- Volatility appears {'high' if abs(market_data['change_percent']) > 1 else 'moderate'}
"""
            
            return CallToolResult(
                content=[
                    TextContent(type="text", text=analysis),
                    TextContent(type="text", text=f"Raw Data: {json.dumps(market_data, indent=2)}")
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error fetching market data: {str(e)}")],
                isError=True
            )

    async def _get_options_chain(self, args: dict) -> CallToolResult:
        """Get options chain data"""
        try:
            options_data = self.zerodha_service.get_options_chain()
            
            # Format options chain display
            chain_display = "📈 **NIFTY 50 OPTIONS CHAIN**\n\n"
            chain_display += f"{'Strike':<8} {'Call LTP':<10} {'Call Vol':<12} {'Put LTP':<10} {'Put Vol':<12}\n"
            chain_display += "-" * 60 + "\n"
            
            for option in options_data:
                chain_display += f"{option.strike_price:<8.0f} "
                chain_display += f"₹{option.call_ltp:<9.2f} "
                chain_display += f"{option.call_volume:<12,} "
                chain_display += f"₹{option.put_ltp:<9.2f} "
                chain_display += f"{option.put_volume:<12,}\n"
            
            # Add analysis
            analysis = "\n**Options Analysis:**\n"
            max_call_volume = max(opt.call_volume for opt in options_data)
            max_put_volume = max(opt.put_volume for opt in options_data)
            
            high_call_vol = [opt for opt in options_data if opt.call_volume > max_call_volume * 0.8]
            high_put_vol = [opt for opt in options_data if opt.put_volume > max_put_volume * 0.8]
            
            if high_call_vol:
                analysis += f"- High Call activity at strikes: {', '.join([str(int(opt.strike_price)) for opt in high_call_vol])}\n"
            if high_put_vol:
                analysis += f"- High Put activity at strikes: {', '.join([str(int(opt.strike_price)) for opt in high_put_vol])}\n"
            
            return CallToolResult(
                content=[
                    TextContent(type="text", text=chain_display + analysis),
                    TextContent(type="text", text=f"Raw Data: {json.dumps([asdict(opt) for opt in options_data], indent=2)}")
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error fetching options chain: {str(e)}")],
                isError=True
            )

    async def _generate_ai_signal(self, args: dict) -> CallToolResult:
        """Generate AI trading signal"""
        try:
            confidence_threshold = args.get("confidence_threshold", 75)
            signal_type = args.get("signal_type", "BOTH")
            
            # Get market data
            quote = self.zerodha_service.get_nifty_quote()
            current_price = quote["last_price"]
            volume = quote["volume"]
            
            # Generate technical indicators
            indicators = self.ai_service.calculate_technical_indicators(current_price, volume)
            conditions = self.ai_service.analyze_market_conditions(indicators)
            
            # Generate signal
            signal = self.ai_service.generate_trading_signal(current_price, indicators, conditions)
            
            if signal.confidence < confidence_threshold:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"No signals above {confidence_threshold}% confidence threshold. Current highest confidence: {signal.confidence}%")]
                )
            
            if signal_type != "BOTH" and signal.type != signal_type:
                # Generate another signal of the requested type
                signal.type = signal_type
                signal.reasoning = f"Generated {signal_type} signal as requested. " + signal.reasoning
            
            signal_display = f"""
🚨 **AI TRADING SIGNAL GENERATED** 🚨

**Signal Type:** {signal.type}
**Strike Price:** ₹{signal.strike_price}
**Confidence:** {signal.confidence}%
**Expiry:** {signal.expiry_date}

**Price Targets:**
- Entry: Current market price
- Target: ₹{signal.target_price}
- Stop Loss: ₹{signal.stop_loss}

**AI Analysis:**
{signal.reasoning}

**Technical Indicators:**
- RSI: {indicators['rsi']:.1f}
- SMA20: ₹{indicators['sma20']:.2f}
- SMA50: ₹{indicators['sma50']:.2f}
- Volatility: {indicators['volatility']:.1f}%

**Market Conditions:**
- Trend: {conditions['trend'].upper()}
- Strength: {conditions['strength']:.1f}/100
- Momentum: {conditions['momentum']:.1f}/100

⚠️ **Risk Warning:** This is an AI-generated signal. Please perform your own analysis and trade responsibly.
"""
            
            return CallToolResult(
                content=[
                    TextContent(type="text", text=signal_display),
                    TextContent(type="text", text=f"Signal Data: {json.dumps(asdict(signal), indent=2)}")
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error generating AI signal: {str(e)}")],
                isError=True
            )

    async def _analyze_trade_opportunity(self, args: dict) -> CallToolResult:
        """Analyze specific trade opportunity"""
        try:
            strike_price = args["strike_price"]
            option_type = args["option_type"]
            capital = args.get("capital", 10000)
            
            # Get current market data
            quote = self.zerodha_service.get_nifty_quote()
            current_price = quote["last_price"]
            
            # Get options data
            options_chain = self.zerodha_service.get_options_chain()
            target_option = next((opt for opt in options_chain if opt.strike_price == strike_price), None)
            
            if not target_option:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Strike price {strike_price} not found in options chain")],
                    isError=True
                )
            
            # Calculate analysis
            option_premium = target_option.call_ltp if option_type == "CALL" else target_option.put_ltp
            moneyness = (current_price - strike_price) / strike_price * 100
            
            # Risk analysis
            max_lots = int(capital / (option_premium * 50))  # Assuming lot size of 50
            total_cost = max_lots * option_premium * 50
            
            # Probability analysis
            if option_type == "CALL":
                profit_prob = 60 if moneyness > -2 else 40
                breakeven = strike_price + option_premium
            else:
                profit_prob = 60 if moneyness < 2 else 40
                breakeven = strike_price - option_premium
            
            analysis = f"""
📊 **TRADE OPPORTUNITY ANALYSIS**

**Option Details:**
- Strike: ₹{strike_price}
- Type: {option_type}
- Current Premium: ₹{option_premium:.2f}
- Volume: {target_option.call_volume if option_type == 'CALL' else target_option.put_volume:,}

**Market Position:**
- Nifty Current: ₹{current_price:.2f}
- Moneyness: {moneyness:+.2f}%
- Status: {'ITM' if (option_type == 'CALL' and moneyness > 0) or (option_type == 'PUT' and moneyness < 0) else 'OTM'}

**Capital Allocation:**
- Available Capital: ₹{capital:,}
- Max Lots: {max_lots}
- Total Cost: ₹{total_cost:,.2f}
- Capital Utilization: {(total_cost/capital)*100:.1f}%

**Risk Metrics:**
- Breakeven: ₹{breakeven:.2f}
- Max Loss: ₹{total_cost:,.2f} (100% of premium)
- Profit Probability: {profit_prob}%

**Recommendation:**
{'✅ GOOD OPPORTUNITY' if profit_prob >= 55 and total_cost/capital <= 0.8 else '⚠️ MODERATE RISK' if profit_prob >= 45 else '❌ HIGH RISK'}

**Entry Strategy:**
- Wait for premium to dip by 5-10%
- Enter in smaller quantities first
- Scale in if trade moves favorably

**Exit Strategy:**
- Take profit at 50-100% gain
- Cut losses at 30-50% of premium
- Time decay acceleration after 2 weeks to expiry
"""
            
            return CallToolResult(
                content=[TextContent(type="text", text=analysis)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing trade opportunity: {str(e)}")],
                isError=True
            )

    async def _risk_management_analysis(self, args: dict) -> CallToolResult:
        """Calculate risk management metrics"""
        try:
            entry_price = args["entry_price"]
            target_price = args["target_price"]
            stop_loss = args["stop_loss"]
            capital = args["capital"]
            risk_percentage = args.get("risk_percentage", 2)
            
            # Calculate metrics
            risk_per_unit = entry_price - stop_loss
            reward_per_unit = target_price - entry_price
            risk_reward_ratio = reward_per_unit / risk_per_unit if risk_per_unit > 0 else 0
            
            max_risk_amount = capital * (risk_percentage / 100)
            max_quantity = int(max_risk_amount / abs(risk_per_unit)) if risk_per_unit != 0 else 0
            
            # Position sizing (assuming lot size of 50)
            lot_size = 50
            max_lots = max_quantity // lot_size
            actual_quantity = max_lots * lot_size
            actual_risk = actual_quantity * abs(risk_per_unit)
            
            total_investment = actual_quantity * entry_price
            potential_profit = actual_quantity * reward_per_unit
            
            analysis = f"""
⚖️ **RISK MANAGEMENT ANALYSIS**

**Trade Parameters:**
- Entry Price: ₹{entry_price:.2f}
- Target Price: ₹{target_price:.2f}
- Stop Loss: ₹{stop_loss:.2f}

**Risk Metrics:**
- Risk per Unit: ₹{abs(risk_per_unit):.2f}
- Reward per Unit: ₹{reward_per_unit:.2f}
- Risk:Reward Ratio: 1:{risk_reward_ratio:.2f}

**Position Sizing:**
- Available Capital: ₹{capital:,}
- Risk Tolerance: {risk_percentage}% = ₹{max_risk_amount:,.2f}
- Maximum Lots: {max_lots}
- Actual Quantity: {actual_quantity}

**Financial Impact:**
- Total Investment: ₹{total_investment:,.2f}
- Actual Risk: ₹{actual_risk:,.2f}
- Potential Profit: ₹{potential_profit:,.2f}
- Capital at Risk: {(actual_risk/capital)*100:.1f}%

**Risk Assessment:**
{'✅ EXCELLENT R:R' if risk_reward_ratio >= 2 else '✅ GOOD R:R' if risk_reward_ratio >= 1.5 else '⚠️ MODERATE R:R' if risk_reward_ratio >= 1 else '❌ POOR R:R'}

**Position Management:**
- Never risk more than {risk_percentage}% on single trade
- Use trailing stops once profit reaches 1:1
- Consider partial profit booking at 1:1.5
- Review stop loss if trade moves favorably

**Kelly Criterion:** {((risk_reward_ratio * 0.6) - 0.4) / risk_reward_ratio * 100:.1f}% of capital
(Assuming 60% win rate)
"""
            
            return CallToolResult(
                content=[TextContent(type="text", text=analysis)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error in risk analysis: {str(e)}")],
                isError=True
            )

    async def _market_sentiment_analysis(self, args: dict) -> CallToolResult:
        """Analyze market sentiment"""
        try:
            timeframe = args.get("timeframe", "15min")
            
            # Get market data
            quote = self.zerodha_service.get_nifty_quote()
            current_price = quote["last_price"]
            change = quote["change"]
            volume = quote["volume"]
            
            # Calculate sentiment indicators
            price_momentum = "bullish" if change > 0 else "bearish" if change < 0 else "neutral"
            volume_analysis = "high" if volume > 1200000 else "normal" if volume > 800000 else "low"
            
            # Generate sentiment score (0-100)
            sentiment_score = 50  # Base neutral
            
            # Price movement impact
            if abs(change) > 100:
                sentiment_score += 20 if change > 0 else -20
            elif abs(change) > 50:
                sentiment_score += 10 if change > 0 else -10
            
            # Volume impact
            if volume > 1200000:
                sentiment_score += 10 if change > 0 else -10
            
            # Technical indicators
            indicators = self.ai_service.calculate_technical_indicators(current_price, volume)
            rsi = indicators['rsi']
            
            if rsi > 70:
                sentiment_score -= 15  # Overbought
            elif rsi < 30:
                sentiment_score += 15  # Oversold
            
            sentiment_score = max(0, min(100, sentiment_score))
            
            # Sentiment classification
            if sentiment_score >= 70:
                sentiment_label = "VERY BULLISH 🚀"
                color = "🟢"
            elif sentiment_score >= 60:
                sentiment_label = "BULLISH 📈"
                color = "🟢"
            elif sentiment_score >= 40:
                sentiment_label = "NEUTRAL ➡️"
                color = "🟡"
            elif sentiment_score >= 30:
                sentiment_label = "BEARISH 📉"
                color = "🔴"
            else:
                sentiment_label = "VERY BEARISH 💥"
                color = "🔴"
            
            analysis = f"""
🎯 **MARKET SENTIMENT ANALYSIS** ({timeframe})

{color} **Overall Sentiment: {sentiment_label}**
**Sentiment Score: {sentiment_score}/100**

**Current Market State:**
- Price: ₹{current_price:.2f} ({change:+.2f})
- Momentum: {price_momentum.upper()}
- Volume: {volume:,} ({volume_analysis})

**Technical Indicators:**
- RSI: {rsi:.1f} ({'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Normal'})
- SMA20: ₹{indicators['sma20']:.2f}
- Volatility: {indicators['volatility']:.1f}%

**Market Signals:**
{'- Strong buying pressure detected' if sentiment_score > 70 else '- Mild buying interest' if sentiment_score > 60 else '- Market consolidation' if sentiment_score > 40 else '- Selling pressure building' if sentiment_score > 30 else '- Strong selling pressure'}
- Volume {'confirms the move' if volume > 1000000 else 'is moderate' if volume > 800000 else 'is low - be cautious'}
- {'Trend continuation likely' if abs(change) > 50 else 'Range-bound movement expected'}

**Trading Implications:**
{'- Favorable for CALL options' if sentiment_score > 60 else '- Favorable for PUT options' if sentiment_score < 40 else '- Mixed signals - trade with caution'}
{'- High conviction trades recommended' if sentiment_score > 70 or sentiment_score < 30 else '- Moderate position sizes advised'}
- Stop losses are crucial in current conditions

**Next Levels to Watch:**
- Support: ₹{current_price - 50:.0f}
- Resistance: ₹{current_price + 50:.0f}
"""
            
            return CallToolResult(
                content=[TextContent(type="text", text=analysis)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error in sentiment analysis: {str(e)}")],
                isError=True
            )

    # Prompt implementation methods
    async def _get_trading_strategy_prompt(self, args: dict) -> GetPromptResult:
        market_outlook = args["market_outlook"]
        risk_tolerance = args["risk_tolerance"]
        capital = args["capital"]
        
        prompt_text = f"""
You are an expert options trader specializing in Nifty 50. Generate a comprehensive trading strategy based on:

Market Outlook: {market_outlook}
Risk Tolerance: {risk_tolerance}
Available Capital: ₹{capital:,}

Provide a detailed strategy including:
1. Market analysis and rationale
2. Specific options strategies to employ
3. Position sizing and risk management
4. Entry and exit criteria
5. Timeline and milestones
6. Risk scenarios and contingency plans

Make the strategy actionable and specific to current market conditions.
"""
        
        return GetPromptResult(
            description="Comprehensive trading strategy based on market outlook and risk profile",
            messages=[
                PromptMessage(
                    role=Role.user,
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )

    async def _get_technical_analysis_prompt(self, args: dict) -> GetPromptResult:
        timeframe = args.get("timeframe", "15min")
        
        # Get current market data for context
        quote = self.zerodha_service.get_nifty_quote()
        current_price = quote["last_price"]
        
        prompt_text = f"""
Perform a detailed technical analysis of Nifty 50 with the following data:

Current Price: ₹{current_price:.2f}
Change: {quote['change']:+.2f}
Volume: {quote['volume']:,}
Timeframe: {timeframe}

Analyze:
1. Price action and trend analysis
2. Support and resistance levels
3. Volume analysis and its implications
4. Momentum indicators
5. Pattern recognition
6. Short-term and medium-term outlook
7. Key levels to watch for trading opportunities

Provide specific price targets and risk levels for both bullish and bearish scenarios.
"""
        
        return GetPromptResult(
            description=f"Technical analysis of Nifty 50 for {timeframe} timeframe",
            messages=[
                PromptMessage(
                    role=Role.user,
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )

    async def _get_options_strategy_prompt(self, args: dict) -> GetPromptResult:
        market_direction = args["market_direction"]
        volatility_expectation = args["volatility_expectation"]
        
        # Get options chain for context
        options_chain = self.zerodha_service.get_options_chain()
        
        prompt_text = f"""
Design optimal options trading strategies based on:

Market Direction: {market_direction}
Volatility Expectation: {volatility_expectation}

Available strikes and premiums:
"""
        for opt in options_chain[:5]:  # Show first 5 strikes
            prompt_text += f"₹{opt.strike_price}: Call ₹{opt.call_ltp:.2f}, Put ₹{opt.put_ltp:.2f}\n"

        prompt_text += """
Recommend:
1. Best options strategies for the given outlook
2. Specific strike selection rationale
3. Optimal entry timing
4. Profit targets and stop losses
5. Time decay management
6. Adjustment strategies if market moves against position
7. Position sizing recommendations

Consider both simple and complex strategies (spreads, straddles, etc.).
"""
        
        return GetPromptResult(
            description="Options strategies recommendation based on market outlook",
            messages=[
                PromptMessage(
                    role=Role.user,
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )

    async def run(self):
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                InitializationOptions(
                    server_name="zerodha-trading-ai",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

async def main():
    """Main entry point"""
    mcp_server = ZerodhaTradingMCP()
    await mcp_server.run()

if __name__ == "__main__":
    asyncio.run(main())
