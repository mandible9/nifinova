#!/usr/bin/env python3
import os
import signal
import sys
from app import app, socketio, ai_service

def signal_handler(sig, frame):
    print('\nShutting down server...')
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start AI signal generation
    ai_service.start_signal_generation()
    
    print("Starting Nifty AI Trading Assistant...")
    print("Real-time updates: Every 1 second")
    print("Access at: http://localhost:5000")
    print("Login: admin/admin")
    print("Press Ctrl+C to stop")
    
    try:
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=5000, 
            debug=False, 
            allow_unsafe_werkzeug=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)