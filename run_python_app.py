#!/usr/bin/env python3
"""
Nifty AI Trading Assistant - Python Application Runner
Real-time data updates every 1 second
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the Flask application
if __name__ == "__main__":
    from app import app, socketio, ai_service
    
    # Start AI signal generation
    ai_service.start_signal_generation()
    
    # Run the Flask-SocketIO application
    print("Starting Nifty AI Trading Assistant (Python)...")
    print("Real-time data updates: Every 1 second")
    print("URL: http://localhost:5000")
    print("Login: admin/admin")
    
    socketio.run(
        app, 
        host='localhost', 
        port=5000, 
        debug=False, 
        allow_unsafe_werkzeug=True
    )