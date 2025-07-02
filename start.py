#!/usr/bin/env python3
"""
Quick start script for Simple Browser Camera
"""

import subprocess
import sys
import webbrowser
import time

def main():
    print("=" * 50)
    print("📷 SIMPLE BROWSER CAMERA")
    print("=" * 50)
    print()
    print("Starting server...")
    
    try:
        # Start the server
        subprocess.Popen([sys.executable, "simple_camera.py"])
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Open browser
        print("Opening browser...")
        webbrowser.open('http://localhost:3000')
        
        print()
        print("✅ Server started successfully!")
        print("🌐 Access at: http://localhost:3000")
        print("📷 Click 'Start Camera' to begin")
        print()
        print("Press Ctrl+C to stop the server")
        
        # Keep script running
        input("Press Enter to stop the server...")
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
