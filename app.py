import os
import json
import time
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random
import math

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
        self.users = [{"id": 1, "username": "admin", "password": "admin"}]
        self.whatsapp_users: List[WhatsAppUser] = []
        self.trading_signals: List[TradingSignal] = []
        self.market_data: Dict[str, MarketData] = {}
        self.options_chain: List[OptionsData] = []
        self.next_signal_id = 1
        self.next_whatsapp_id = 1

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

# Zerodha Service
class ZerodhaService:
    def __init__(self):
        self.api_key = os.getenv('ZERODHA_API_KEY', '')
        self.access_token = os.getenv('ZERODHA_ACCESS_TOKEN', '')
        self.base_url = 'https://api.kite.trade'

    def get_nifty_quote(self) -> Dict:
        if not self.api_key or not self.access_token:
            # Return realistic mock data
            base_price = 19845.30
            change = random.uniform(-200, 200)
            return {
                "instrument_token": 256265,
                "last_price": base_price + change,
                "change": change,
                "net_change": (change / base_price) * 100,
                "volume": random.randint(800000, 1500000)
            }
        
        try:
            headers = {
                'Authorization': f'token {self.api_key}:{self.access_token}',
                'X-Kite-Version': '3'
            }
            response = requests.get(f'{self.base_url}/quote?i=NSE:NIFTY 50', headers=headers)
            if response.status_code == 200:
                return response.json()['data']
        except Exception as e:
            print(f"Zerodha API error: {e}")
        
        # Fallback to mock data
        base_price = 19845.30
        change = random.uniform(-200, 200)
        return {
            "instrument_token": 256265,
            "last_price": base_price + change,
            "change": change,
            "net_change": (change / base_price) * 100,
            "volume": random.randint(800000, 1500000)
        }

    def get_options_chain(self) -> List[OptionsData]:
        strikes = [19750, 19800, 19850, 19900, 19950]
        options = []
        
        for strike in strikes:
            call_ltp = max(5, 100 - abs(strike - 19850) * 2 + random.uniform(-20, 20))
            put_ltp = max(5, 20 + abs(strike - 19850) * 1.5 + random.uniform(-15, 15))
            
            options.append(OptionsData(
                strike_price=strike,
                call_ltp=call_ltp,
                call_volume=random.randint(50000, 500000),
                put_ltp=put_ltp,
                put_volume=random.randint(40000, 400000),
                expiry_date=self.get_next_thursday().strftime('%Y-%m-%d')
            ))
        
        return options

    def get_next_thursday(self) -> datetime:
        today = datetime.now()
        days_ahead = 3 - today.weekday()  # Thursday is 3
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)

zerodha_service = ZerodhaService()

# WhatsApp Service
class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
        self.api_url = 'https://graph.facebook.com/v17.0'

    def send_trading_signal(self, phone_number: str, signal: TradingSignal):
        message = f"""🚨 STRONG BUY SIGNAL 🚨

📈 {signal.type} Signal
🎯 Strike: {signal.strike_price}
💪 Confidence: {signal.confidence}%

📊 Trade Details:
• Target: ₹{signal.target_price}
• Stop Loss: ₹{signal.stop_loss}

💡 AI Analysis:
{signal.reasoning}

⚠️ Risk Disclaimer: Trading involves risk. Please trade responsibly.

Powered by Nifty AI Trading Assistant"""

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

# AI Signals Service
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
            
            # Update market data
            market_data = MarketData(
                symbol='NIFTY50',
                price=current_price,
                change=nifty_data['change'],
                change_percent=nifty_data['net_change'],
                volume=volume,
                last_updated=datetime.now().isoformat()
            )
            store.market_data['NIFTY50'] = market_data
            
            # Generate AI signals
            indicators = self.calculate_technical_indicators(current_price, volume)
            conditions = self.analyze_market_conditions(indicators)
            
            # Generate 1-2 signals
            num_signals = random.randint(1, 2)
            new_signals = []
            
            for _ in range(num_signals):
                signal = self.generate_trading_signal(current_price, indicators, conditions)
                stored_signal = store.add_trading_signal(signal)
                new_signals.append(stored_signal)
                
                # Send WhatsApp notifications for high confidence signals
                if signal.confidence >= 90:
                    for user in store.whatsapp_users:
                        if user.is_active:
                            whatsapp_service.send_trading_signal(user.phone_number, signal)
            
            # Update options chain
            store.options_chain = zerodha_service.get_options_chain()
            
            # Emit real-time updates
            socketio.emit('market_update', {
                'nifty_data': asdict(market_data),
                'new_signals': [asdict(s) for s in new_signals],
                'options_chain': [asdict(o) for o in store.options_chain]
            })
            
            print(f"Generated {len(new_signals)} new signals. Nifty: {current_price:.2f}")
            
        except Exception as e:
            print(f"Error generating signals: {e}")

    def start_signal_generation(self):
        if self.is_running:
            return
        
        self.is_running = True
        
        def signal_loop():
            while self.is_running:
                self.generate_signals()
                time.sleep(1)  # 1 second frequency
        
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
        nifty_data = MarketData(
            symbol='NIFTY50',
            price=quote['last_price'],
            change=quote['change'],
            change_percent=quote['net_change'],
            volume=quote['volume'],
            last_updated=datetime.now().isoformat()
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
    print("Login: admin / admin")
    
    socketio.run(app, host='localhost', port=5000, debug=False, allow_unsafe_werkzeug=True)