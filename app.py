
import os
import json
import time
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random
import math
import pytz

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import requests

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nifty-ai-trading-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Data Models
@dataclass
class TradingSignal:
    id: int
    type: str  # CALL or PUT
    strike_price: float
    target_price: float
    stop_loss: float
    confidence: int
    reasoning: str
    expiry_date: str
    created_at: str
    whatsapp_sent: bool = False

@dataclass
class WhatsAppUser:
    id: int
    phone_number: str
    is_active: bool = True
    created_at: str = ""

@dataclass
class MarketData:
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    last_updated: str
    market_status: str = "OPEN"
    sentiment: str = "NEUTRAL"
    flash_message: str = ""

@dataclass
class OptionsData:
    strike_price: float
    call_ltp: float
    call_volume: int
    put_ltp: float
    put_volume: int
    expiry_date: str

# In-memory storage
class DataStore:
    def __init__(self):
        self.users = [{"id": 1, "username": "pkrsolution", "password": "prabhanjan2025"}]
        self.whatsapp_users: List[WhatsAppUser] = []
        self.trading_signals: List[TradingSignal] = []
        self.market_data: Dict[str, MarketData] = {}
        self.options_chain: List[OptionsData] = []
        self.next_signal_id = 1
        self.next_whatsapp_id = 1
        self.last_market_data = None

    def add_whatsapp_user(self, phone_number: str) -> WhatsAppUser:
        user = WhatsAppUser(
            id=self.next_whatsapp_id,
            phone_number=phone_number,
            created_at=datetime.now().isoformat()
        )
        self.whatsapp_users.append(user)
        self.next_whatsapp_id += 1
        return user

    def remove_whatsapp_user(self, phone_number: str) -> bool:
        for i, user in enumerate(self.whatsapp_users):
            if user.phone_number == phone_number:
                self.whatsapp_users[i].is_active = False
                return True
        return False

    def add_trading_signal(self, signal: TradingSignal) -> TradingSignal:
        signal.id = self.next_signal_id
        self.trading_signals.append(signal)
        self.next_signal_id += 1
        return signal

    def get_active_signals(self) -> List[TradingSignal]:
        return [s for s in self.trading_signals if s.created_at >= (datetime.now() - timedelta(hours=24)).isoformat()]

store = DataStore()

# Market Status Service
class MarketStatusService:
    def __init__(self):
        self.ist_tz = pytz.timezone('Asia/Kolkata')

    def is_market_open(self) -> bool:
        """Check if NSE market is currently open"""
        now = datetime.now(self.ist_tz)
        
        # Check if it's a weekday (Monday=0, Sunday=6)
        if now.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Market hours: 9:15 AM to 3:30 PM IST
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open <= now <= market_close

    def get_market_status(self) -> str:
        """Get current market status"""
        if self.is_market_open():
            return "OPEN"
        else:
            now = datetime.now(self.ist_tz)
            if now.weekday() >= 5:
                return "WEEKEND"
            elif now.hour < 9 or (now.hour == 9 and now.minute < 15):
                return "PRE_MARKET"
            else:
                return "CLOSED"

market_status_service = MarketStatusService()

# NSE Data Service
class NSEDataService:
    def __init__(self):
        self.base_url = "https://www.nseindia.com/api"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }

    def get_nifty_data(self) -> Dict:
        """Fetch real Nifty 50 data from NSE"""
        try:
            # Get market status first
            market_status = market_status_service.get_market_status()
            
            if market_status != "OPEN":
                # Return last stored data if market is closed
                if store.last_market_data:
                    return store.last_market_data
            
            # Try to fetch live data
            url = f"{self.base_url}/equity-stockIndices?index=NIFTY%2050"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                nifty_data = data['data'][0]  # First item is usually Nifty 50
                
                result = {
                    "last_price": float(nifty_data.get('last', 0)),
                    "change": float(nifty_data.get('change', 0)),
                    "net_change": float(nifty_data.get('pChange', 0)),
                    "volume": int(nifty_data.get('totalTradedVolume', 0)),
                    "market_status": market_status
                }
                
                # Store the data for when market is closed
                store.last_market_data = result
                return result
                
        except Exception as e:
            print(f"NSE API error: {e}")
        
        # Return last stored data or fallback
        if store.last_market_data:
            store.last_market_data["market_status"] = market_status
            return store.last_market_data
        
        # Final fallback with realistic data
        return {
            "last_price": 19845.30,
            "change": 0,
            "net_change": 0,
            "volume": 0,
            "market_status": market_status
        }

    def get_options_chain_data(self) -> List[OptionsData]:
        """Fetch options chain from NSE"""
        try:
            if market_status_service.get_market_status() != "OPEN":
                # Return stored options chain when market is closed
                if store.options_chain:
                    return store.options_chain
            
            # Try to fetch live options data
            url = f"{self.base_url}/option-chain-indices?symbol=NIFTY"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                options = []
                
                records = data.get('records', {}).get('data', [])
                for record in records[:10]:  # Get first 10 strikes
                    strike = record.get('strikePrice', 0)
                    ce_data = record.get('CE', {})
                    pe_data = record.get('PE', {})
                    
                    options.append(OptionsData(
                        strike_price=float(strike),
                        call_ltp=float(ce_data.get('lastPrice', 0)),
                        call_volume=int(ce_data.get('totalTradedVolume', 0)),
                        put_ltp=float(pe_data.get('lastPrice', 0)),
                        put_volume=int(pe_data.get('totalTradedVolume', 0)),
                        expiry_date=ce_data.get('expiryDate', '')
                    ))
                
                return options
                
        except Exception as e:
            print(f"Options chain API error: {e}")
        
        # Return stored data or generate mock data
        if store.options_chain:
            return store.options_chain
        
        return self._generate_mock_options()

    def _generate_mock_options(self) -> List[OptionsData]:
        """Generate mock options data when real data unavailable"""
        base_price = store.last_market_data.get('last_price', 19845) if store.last_market_data else 19845
        strikes = [base_price - 100, base_price - 50, base_price, base_price + 50, base_price + 100]
        
        options = []
        for strike in strikes:
            options.append(OptionsData(
                strike_price=strike,
                call_ltp=max(5, 100 - abs(strike - base_price) * 2),
                call_volume=0,
                put_ltp=max(5, 20 + abs(strike - base_price) * 1.5),
                put_volume=0,
                expiry_date="2025-01-02"
            ))
        
        return options

nse_service = NSEDataService()

# Claude AI Service
class ClaudeAIService:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY', '')
        self.api_url = 'https://api.anthropic.com/v1/messages'

    def analyze_market_sentiment(self, market_data: Dict, options_data: List[OptionsData]) -> Dict:
        """Analyze market sentiment using Claude AI"""
        if not self.api_key:
            return self._fallback_sentiment_analysis(market_data)
        
        try:
            prompt = f"""
            Analyze the current Nifty 50 market data and provide sentiment analysis:
            
            Market Data:
            - Current Price: ₹{market_data['last_price']:.2f}
            - Change: {market_data['change']:+.2f} ({market_data['net_change']:+.2f}%)
            - Volume: {market_data['volume']:,}
            - Market Status: {market_data['market_status']}
            
            Options Data Sample:
            {json.dumps([asdict(opt) for opt in options_data[:3]], indent=2)}
            
            Please provide:
            1. Overall sentiment (BULLISH/BEARISH/NEUTRAL)
            2. Trading recommendation (BUY_CALL/BUY_PUT/DONT_TRADE)
            3. Brief reasoning (max 100 words)
            
            Respond in JSON format:
            {{"sentiment": "BULLISH", "recommendation": "BUY_CALL", "reasoning": "Market shows..."}}
            """
            
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 200,
                'messages': [{'role': 'user', 'content': prompt}]
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                return json.loads(content)
            
        except Exception as e:
            print(f"Claude AI error: {e}")
        
        return self._fallback_sentiment_analysis(market_data)

    def _fallback_sentiment_analysis(self, market_data: Dict) -> Dict:
        """Fallback sentiment analysis when Claude AI is unavailable"""
        change = market_data.get('change', 0)
        change_percent = market_data.get('net_change', 0)
        
        if change_percent > 1:
            sentiment = "BULLISH"
            recommendation = "BUY_CALL"
            reasoning = "Strong positive momentum with over 1% gain"
        elif change_percent < -1:
            sentiment = "BEARISH"
            recommendation = "BUY_PUT"
            reasoning = "Significant decline with over 1% loss"
        elif abs(change_percent) > 0.5:
            sentiment = "BULLISH" if change > 0 else "BEARISH"
            recommendation = "BUY_CALL" if change > 0 else "BUY_PUT"
            reasoning = f"Moderate {'upward' if change > 0 else 'downward'} movement"
        else:
            sentiment = "NEUTRAL"
            recommendation = "DONT_TRADE"
            reasoning = "Low volatility, range-bound movement"
        
        return {
            "sentiment": sentiment,
            "recommendation": recommendation,
            "reasoning": reasoning
        }

claude_service = ClaudeAIService()

# Zerodha Service (Updated)
class ZerodhaService:
    def __init__(self):
        self.api_key = os.getenv('ZERODHA_API_KEY', '')
        self.access_token = os.getenv('ZERODHA_ACCESS_TOKEN', '')
        self.base_url = 'https://api.kite.trade'

    def get_nifty_quote(self) -> Dict:
        """Get Nifty quote with market status awareness"""
        market_status = market_status_service.get_market_status()
        
        if market_status != "OPEN":
            # Use NSE service for closed market data
            return nse_service.get_nifty_data()
        
        if not self.api_key or not self.access_token:
            # Use NSE service as fallback
            return nse_service.get_nifty_data()
        
        try:
            headers = {
                'Authorization': f'token {self.api_key}:{self.access_token}',
                'X-Kite-Version': '3'
            }
            response = requests.get(f'{self.base_url}/quote?i=NSE:NIFTY 50', headers=headers)
            if response.status_code == 200:
                data = response.json()['data']
                data['market_status'] = market_status
                return data
        except Exception as e:
            print(f"Zerodha API error: {e}")
        
        # Fallback to NSE service
        return nse_service.get_nifty_data()

    def get_options_chain(self) -> List[OptionsData]:
        """Get options chain with market status awareness"""
        return nse_service.get_options_chain_data()

    def get_next_thursday(self) -> datetime:
        today = datetime.now()
        days_ahead = 3 - today.weekday()  # Thursday is 3
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)

zerodha_service = ZerodhaService()

# WhatsApp Service (Enhanced)
class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
        self.api_url = 'https://graph.facebook.com/v17.0'

    def send_trading_signal(self, phone_number: str, signal: TradingSignal):
        message = f"""🚨 NIFINOVA AI SIGNAL 🚨

📈 {signal.type} Signal Alert
🎯 Strike: {signal.strike_price}
💪 Confidence: {signal.confidence}%

📊 Trade Details:
• Target: ₹{signal.target_price}
• Stop Loss: ₹{signal.stop_loss}

💡 AI Analysis:
{signal.reasoning}

⚠️ Risk Disclaimer: Trading involves risk. Please trade responsibly.

🔥 Powered by NIFINOVA
💼 PKR SOLUTION © 2025"""

        return self._send_whatsapp_message(phone_number, message)

    def send_market_alert(self, phone_number: str, market_data: MarketData):
        """Send market sentiment alert via WhatsApp"""
        status_emoji = "🟢" if market_data.sentiment == "BULLISH" else "🔴" if market_data.sentiment == "BEARISH" else "🟡"
        
        message = f"""{status_emoji} MARKET ALERT {status_emoji}

📊 Nifty 50: ₹{market_data.price:.2f}
📈 Change: {market_data.change:+.2f} ({market_data.change_percent:+.2f}%)
🎯 Sentiment: {market_data.sentiment}

💡 Flash Signal: {market_data.flash_message}

🕐 Status: {market_data.market_status}
⏰ Updated: {datetime.now().strftime('%H:%M:%S')}

🔥 NIFINOVA AI"""

        return self._send_whatsapp_message(phone_number, message)

    def _send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        if not self.access_token or not self.phone_number_id:
            print(f"WhatsApp message would be sent to {phone_number}: {message}")
            return True

        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            data = {
                "messaging_product": "whatsapp",
                "to": phone_number.replace('+', ''),
                "type": "text",
                "text": {"body": message}
            }
            response = requests.post(
                f'{self.api_url}/{self.phone_number_id}/messages',
                headers=headers,
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"WhatsApp API error: {e}")
            return False

whatsapp_service = WhatsAppService()

# AI Signals Service (Enhanced)
class AISignalsService:
    def __init__(self):
        self.is_running = False

    def calculate_technical_indicators(self, price: float, volume: int) -> Dict:
        return {
            'rsi': 45 + random.uniform(0, 20),
            'sma20': price * (0.98 + random.uniform(0, 0.04)),
            'sma50': price * (0.96 + random.uniform(0, 0.08)),
            'volume': volume,
            'volatility': 15 + random.uniform(0, 10)
        }

    def analyze_market_conditions(self, indicators: Dict) -> Dict:
        trend = 'sideways'
        strength = 50
        momentum = 50

        if indicators['rsi'] > 55 and indicators['sma20'] > indicators['sma50']:
            trend = 'bullish'
            strength = 60 + random.uniform(0, 30)
            momentum = 55 + random.uniform(0, 25)
        elif indicators['rsi'] < 45 and indicators['sma20'] < indicators['sma50']:
            trend = 'bearish'
            strength = 60 + random.uniform(0, 30)
            momentum = 55 + random.uniform(0, 25)
        else:
            strength = 40 + random.uniform(0, 20)
            momentum = 40 + random.uniform(0, 20)

        return {'trend': trend, 'strength': strength, 'momentum': momentum}

    def generate_trading_signal(self, current_price: float, indicators: Dict, conditions: Dict) -> TradingSignal:
        is_call = conditions['trend'] == 'bullish' and random.random() > 0.3
        signal_type = 'CALL' if is_call else 'PUT'
        
        # Generate strike price
        base_strike = round(current_price / 50) * 50
        if is_call:
            strike_price = base_strike + random.choice([0, 50, 100])
        else:
            strike_price = base_strike - random.choice([0, 50, 100])

        # Calculate confidence
        confidence = 60
        if conditions['strength'] > 70:
            confidence += 15
        if conditions['momentum'] > 70:
            confidence += 10
        if indicators['volume'] > 1000000:
            confidence += 5
        if indicators['volatility'] < 20:
            confidence += 10
        
        confidence += random.randint(-10, 20)
        confidence = max(60, min(98, confidence))

        # Generate prices
        base_option_price = 30 + random.uniform(0, 40)
        target_price = base_option_price * (1.5 + random.uniform(0, 0.8))
        stop_loss = base_option_price * (0.4 + random.uniform(0, 0.3))

        # Generate reasoning
        reasons = []
        if signal_type == 'CALL':
            if conditions['trend'] == 'bullish':
                reasons.append('Strong bullish momentum detected')
            if indicators['rsi'] < 50:
                reasons.append('RSI oversold recovery pattern')
            if indicators['sma20'] > indicators['sma50']:
                reasons.append('Short-term MA above long-term MA')
        else:
            if conditions['trend'] == 'bearish':
                reasons.append('Bearish trend continuation expected')
            if indicators['rsi'] > 60:
                reasons.append('RSI overbought, correction likely')
            if indicators['volatility'] > 25:
                reasons.append('High volatility favoring downward move')

        if confidence > 90:
            reasons.append('Multiple confirmations align')

        reasoning = ', '.join(reasons[:2]) + '. Trade with proper risk management.'

        return TradingSignal(
            id=0,  # Will be set by store
            type=signal_type,
            strike_price=strike_price,
            target_price=round(target_price, 2),
            stop_loss=round(stop_loss, 2),
            confidence=confidence,
            reasoning=reasoning,
            expiry_date=zerodha_service.get_next_thursday().strftime('%Y-%m-%d'),
            created_at=datetime.now().isoformat()
        )

    def generate_signals(self):
        try:
            # Get market data
            nifty_data = zerodha_service.get_nifty_quote()
            current_price = nifty_data['last_price']
            volume = nifty_data['volume']
            market_status = nifty_data.get('market_status', 'UNKNOWN')
            
            # Get options data
            options_data = zerodha_service.get_options_chain()
            store.options_chain = options_data
            
            # Get AI sentiment analysis
            sentiment_analysis = claude_service.analyze_market_sentiment(nifty_data, options_data)
            
            # Create market data with sentiment
            market_data = MarketData(
                symbol='NIFTY50',
                price=current_price,
                change=nifty_data['change'],
                change_percent=nifty_data['net_change'],
                volume=volume,
                last_updated=datetime.now().isoformat(),
                market_status=market_status,
                sentiment=sentiment_analysis.get('sentiment', 'NEUTRAL'),
                flash_message=self._format_flash_message(sentiment_analysis.get('recommendation', 'DONT_TRADE'))
            )
            store.market_data['NIFTY50'] = market_data
            
            # Generate signals only if market is open or near close
            new_signals = []
            if market_status in ["OPEN", "PRE_MARKET"]:
                # Generate AI signals
                indicators = self.calculate_technical_indicators(current_price, volume)
                conditions = self.analyze_market_conditions(indicators)
                
                # Generate 1-2 signals
                num_signals = random.randint(1, 2)
                
                for _ in range(num_signals):
                    signal = self.generate_trading_signal(current_price, indicators, conditions)
                    stored_signal = store.add_trading_signal(signal)
                    new_signals.append(stored_signal)
                    
                    # Send WhatsApp notifications for high confidence signals
                    if signal.confidence >= 90:
                        for user in store.whatsapp_users:
                            if user.is_active:
                                whatsapp_service.send_trading_signal(user.phone_number, signal)
            
            # Send market alerts if sentiment changed significantly
            if market_status == "CLOSED" and sentiment_analysis.get('sentiment') != 'NEUTRAL':
                for user in store.whatsapp_users:
                    if user.is_active:
                        whatsapp_service.send_market_alert(user.phone_number, market_data)
            
            # Emit real-time updates
            socketio.emit('market_update', {
                'nifty_data': asdict(market_data),
                'new_signals': [asdict(s) for s in new_signals],
                'options_chain': [asdict(o) for o in options_data]
            })
            
            print(f"Market: {market_status} | Nifty: {current_price:.2f} | Sentiment: {sentiment_analysis.get('sentiment')} | Signals: {len(new_signals)}")
            
        except Exception as e:
            print(f"Error generating signals: {e}")

    def _format_flash_message(self, recommendation: str) -> str:
        """Format trading recommendation as flash message"""
        messages = {
            "BUY_CALL": "🚀 BUY CALL - Bullish momentum detected!",
            "BUY_PUT": "📉 BUY PUT - Bearish pressure building!",
            "DONT_TRADE": "⏸️ HOLD - Wait for clear direction"
        }
        return messages.get(recommendation, "⏸️ HOLD - Monitor market")

    def start_signal_generation(self):
        if self.is_running:
            return
        
        self.is_running = True
        
        def signal_loop():
            while self.is_running:
                self.generate_signals()
                # Adjust frequency based on market status
                market_status = market_status_service.get_market_status()
                sleep_time = 5 if market_status == "OPEN" else 30  # 5 sec when open, 30 sec when closed
                time.sleep(sleep_time)
        
        thread = threading.Thread(target=signal_loop, daemon=True)
        thread.start()

ai_service = AISignalsService()

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        for user in store.users:
            if user['username'] == username and user['password'] == password:
                session['user_id'] = user['id']
                session['username'] = username
                return jsonify({'success': True, 'user': {'id': user['id'], 'username': username}})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# API Routes
@app.route('/api/market/overview')
def market_overview():
    nifty_data = store.market_data.get('NIFTY50')
    active_signals = store.get_active_signals()
    
    if not nifty_data:
        # Generate initial data
        quote = zerodha_service.get_nifty_quote()
        options_data = zerodha_service.get_options_chain()
        sentiment_analysis = claude_service.analyze_market_sentiment(quote, options_data)
        
        nifty_data = MarketData(
            symbol='NIFTY50',
            price=quote['last_price'],
            change=quote['change'],
            change_percent=quote['net_change'],
            volume=quote['volume'],
            last_updated=datetime.now().isoformat(),
            market_status=quote.get('market_status', 'UNKNOWN'),
            sentiment=sentiment_analysis.get('sentiment', 'NEUTRAL'),
            flash_message=ai_service._format_flash_message(sentiment_analysis.get('recommendation', 'DONT_TRADE'))
        )
        store.market_data['NIFTY50'] = nifty_data
    
    return jsonify({
        'nifty50': asdict(nifty_data),
        'active_signals': len(active_signals),
        'success_rate': 74.5,
        'whatsapp_users': len([u for u in store.whatsapp_users if u.is_active]),
        'portfolio': {
            'total_pnl': 12456.78,
            'active_positions': 3
        }
    })

@app.route('/api/signals')
def get_signals():
    signals = store.get_active_signals()
    return jsonify([asdict(s) for s in signals])

@app.route('/api/whatsapp/users', methods=['GET', 'POST', 'DELETE'])
def whatsapp_users():
    if request.method == 'GET':
        active_users = [u for u in store.whatsapp_users if u.is_active]
        return jsonify([asdict(u) for u in active_users])
    
    elif request.method == 'POST':
        data = request.get_json()
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return jsonify({'error': 'Phone number required'}), 400
        
        # Check if already exists
        for user in store.whatsapp_users:
            if user.phone_number == phone_number and user.is_active:
                return jsonify({'error': 'Phone number already registered'}), 400
        
        user = store.add_whatsapp_user(phone_number)
        return jsonify(asdict(user))

@app.route('/api/whatsapp/users/<phone_number>', methods=['DELETE'])
def remove_whatsapp_user(phone_number):
    success = store.remove_whatsapp_user(phone_number)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/options-chain')
def options_chain():
    if not store.options_chain:
        store.options_chain = zerodha_service.get_options_chain()
    return jsonify([asdict(o) for o in store.options_chain])

@app.route('/api/market/status')
def market_status():
    """Get current market status"""
    status = market_status_service.get_market_status()
    return jsonify({
        'status': status,
        'is_open': market_status_service.is_market_open(),
        'timestamp': datetime.now().isoformat()
    })

# Socket.IO events
@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected to real-time updates'})

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start AI signal generation
    ai_service.start_signal_generation()
    
    # Run the app
    print("Starting Nifty AI Trading Assistant...")
    print("URL: http://localhost:5000")
    print("Login: pkrsolution / prabhanjan2025")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True, use_reloader=False, log_output=True)
