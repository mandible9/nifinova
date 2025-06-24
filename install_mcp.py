
#!/usr/bin/env python3

import subprocess
import sys

def install_mcp_dependencies():
    """Install MCP and related dependencies"""
    
    print("🔧 Installing MCP dependencies...")
    
    dependencies = [
        "mcp>=1.0.0",
        "pydantic>=2.0.0", 
        "anyio>=4.0.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
    
    print("\n🎉 All MCP dependencies installed successfully!")
    print("\nYou can now run:")
    print("  • python mcp_server.py (to start the MCP server)")
    print("  • python mcp_client_example.py (to test the server)")
    
    return True

if __name__ == "__main__":
    install_mcp_dependencies()
