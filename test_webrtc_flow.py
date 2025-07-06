#!/usr/bin/env python3
"""
Test script to verify the complete WebRTC flow with OAK camera
"""
import asyncio
import websockets
import json
import time
import requests
from threading import Thread

def test_http_servers():
    """Test if HTTP servers are running"""
    print("🔍 Testing HTTP servers...")
    
    try:
        # Test Flask server
        response = requests.get("http://localhost:8080", timeout=5)
        print(f"✅ Flask server: {response.status_code}")
    except:
        print("❌ Flask server not running")
    
    try:
        # Test OAK client page
        response = requests.get("http://localhost:8080/oak", timeout=5)
        print(f"✅ OAK client page: {response.status_code}")
    except:
        print("❌ OAK client page not accessible")

async def test_signaling_server():
    """Test WebSocket signaling server"""
    print("\n🔍 Testing signaling server...")
    
    try:
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            print("✅ Signaling server connected")
            
            # Test joining a room
            await websocket.send(json.dumps({
                "type": "join_room", 
                "room": "test-room"
            }))
            
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("type") == "room_joined":
                print(f"✅ Room joined: {data.get('room')}")
            else:
                print(f"❓ Unexpected response: {data}")
            
    except Exception as e:
        print(f"❌ Signaling server error: {e}")

async def test_oak_bridge():
    """Test OAK camera bridge"""
    print("\n🔍 Testing OAK camera bridge...")
    
    try:
        uri = "ws://localhost:8766"
        async with websockets.connect(uri) as websocket:
            print("✅ OAK bridge connected")
            
            # Wait for a few frames
            frame_count = 0
            start_time = time.time()
            
            while frame_count < 10 and (time.time() - start_time) < 10:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    if isinstance(message, bytes):
                        frame_count += 1
                        print(f"📸 Received frame {frame_count} ({len(message)} bytes)")
                    else:
                        data = json.loads(message)
                        print(f"📝 JSON message: {data}")
                except asyncio.TimeoutError:
                    print("⏰ No frames received in 2 seconds")
                    break
            
            if frame_count > 0:
                fps = frame_count / (time.time() - start_time)
                print(f"✅ OAK bridge streaming: {fps:.1f} FPS")
            else:
                print("❌ No frames received from OAK bridge")
            
    except Exception as e:
        print(f"❌ OAK bridge error: {e}")

async def main():
    """Run all tests"""
    print("🧪 WebRTC + OAK Camera Flow Test")
    print("=" * 50)
    
    # Test HTTP servers
    test_http_servers()
    
    # Test WebSocket servers
    await test_signaling_server()
    await test_oak_bridge()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print("1. Make sure all servers are running: python start_oak_servers.py")
    print("2. Open browser to: http://localhost:8080/oak")
    print("3. Connect to signaling server")
    print("4. Join a room (e.g., 'oak-room')")
    print("5. Connect OAK camera")
    print("6. Start video")
    print("7. Open second browser tab, join same room")
    print("8. You should see OAK camera stream in remote video!")

if __name__ == "__main__":
    asyncio.run(main())
