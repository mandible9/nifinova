import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🚀 Starting Nifty AI Trading Assistant (Python)")
    print("=" * 60)
    print()
    
    # Check if Python is available
    try:
        python_version = subprocess.check_output([sys.executable, '--version'], 
                                               stderr=subprocess.STDOUT, 
                                               universal_newlines=True)
        print(f"✓ Python: {python_version.strip()}")
    except Exception as e:
        print(f"✗ Python check failed: {e}")
        input("Press Enter to exit...")
        return
    
    # Check if required packages are installed
    required_packages = ['flask', 'flask_socketio', 'requests']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}: Available")
        except ImportError:
            print(f"✗ {package}: Missing")
            print("Installing required packages...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package}: Installed")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                input("Press Enter to exit...")
                return
    
    print()
    print("🔧 Configuration:")
    print("   Host: localhost")
    print("   Port: 5000")
    print("   Login: admin / admin")
    print("   Data Updates: Every 1 second")
    print()
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    
    print("🌐 Starting server...")
    print("   Once started, open: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Import and run the Flask app
        from app import app, socketio
        socketio.run(app, host='localhost', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if port 5000 is already in use")
        print("2. Verify all dependencies are installed")
        print("3. Check Python version compatibility")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()