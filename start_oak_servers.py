#!/usr/bin/env python3
"""
Start All WebRTC with OAK Camera Servers

This script starts all the necessary servers for WebRTC with OAK camera support:
1. WebSocket signaling server (port 8765)
2. OAK camera bridge (port 8766)  
3. HTTP client server (port 5001)
"""

import subprocess
import time
import signal
import sys
import os

def start_server(name, command, check_delay=2):
    """Start a server process"""
    print(f"🚀 Starting {name}...")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        time.sleep(check_delay)
        
        if process.poll() is None:
            print(f"✅ {name} started successfully (PID: {process.pid})")
            return process
        else:
            print(f"❌ {name} failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        return None

def main():
    """Main function"""
    print("🔶 WebRTC with OAK Camera - Server Startup")
    print("=" * 50)
    
    processes = []
    
    try:
        # Start WebSocket signaling server
        p1 = start_server(
            "WebSocket Signaling Server",
            "python websocket_server.py"
        )
        if p1:
            processes.append(p1)
        
        # Start OAK camera bridge
        p2 = start_server(
            "OAK Camera Bridge",
            "python oak_camera_bridge.py"
        )
        if p2:
            processes.append(p2)
        
        # Start HTTP client server
        p3 = start_server(
            "HTTP Client Server",
            "python client_server.py"
        )
        if p3:
            processes.append(p3)
        
        if len(processes) == 3:
            print("\n✅ All servers started successfully!")
            print("\n🌐 Access Points:")
            print("📱 Main Interface: http://localhost:5001")
            print("🔶 OAK Camera Client: http://localhost:5001/oak")
            print("🔗 WebSocket Client: http://localhost:5001/websocket")
            print("📋 Test Instructions: http://localhost:5001/test")
            print("\n🔧 Press Ctrl+C to stop all servers")
            
            # Wait for interrupt
            while True:
                time.sleep(1)
                
        else:
            print(f"\n❌ Only {len(processes)}/3 servers started successfully")
            print("Please check the error messages above")
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Server (PID: {process.pid}) stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚡ Server (PID: {process.pid}) force killed")
            except Exception as e:
                print(f"⚠️ Error stopping server: {e}")
        
        print("🏁 All servers stopped")

if __name__ == "__main__":
    if not os.path.exists("websocket_server.py"):
        print("❌ Error: websocket_server.py not found!")
        print("Make sure you're running this from the correct directory.")
        sys.exit(1)
    
    main()
