#!/usr/bin/env python3
"""
WebRTC Client Server

Serves the sample client HTML file for testing P2P connections.
This allows you to easily test connections from different devices/browsers.
"""

from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def client():
    """Serve the test info page as default"""
    return test_info()

@app.route('/minimal')
def minimal_client():
    """Serve the minimal client"""
    return send_file('clients/minimal_client.html')

@app.route('/mobile')
def mobile_client():
    """Serve the mobile client"""
    return send_file('clients/mobile_client.html')

@app.route('/debug')
def debug_client():
    """Serve the debug client"""
    return send_file('clients/debug_client.html')

@app.route('/screenshare')
def screenshare_client():
    """Serve the screenshare client"""
    return send_file('clients/screenshare_client.html')

@app.route('/websocket')
def websocket_client():
    """Serve the pure WebSocket client"""
    return send_file('clients/websocket_client.html')

@app.route('/oak')
def oak_websocket_client():
    """Serve the WebSocket client with OAK camera support"""
    return send_file('clients/oak_websocket_client.html')

@app.route('/diagnostics')
def diagnostics():
    """Serve the diagnostics page"""
    return send_file('diagnostics.html')

@app.route('/mobile-test')
def mobile_test():
    """Serve the mobile test page"""
    return send_file('mobile_test.html')

@app.route('/test')
def test_info():
    """Test endpoint with connection instructions"""
    return '''
    <h1>🎥 WebRTC Client Test Server</h1>
    <p><strong>Main Client:</strong> <a href="/">http://localhost:8080</a></p>
    <p><strong>Socket.IO Server:</strong> <a href="http://localhost:4000">http://localhost:4000</a></p>
    <p><strong>WebSocket Server:</strong> ws://localhost:8765</p>
    
    <h2>🌐 Available Clients:</h2>
    <ul>
        <li><a href="/minimal">Minimal Client</a> - Simple WebRTC client</li>
        <li><a href="/mobile">Mobile Client</a> - Mobile-optimized interface</li>
        <li><a href="/debug">Debug Client</a> - Detailed logging and diagnostics</li>
        <li><a href="/screenshare">Screenshare Client</a> - Screen sharing demo</li>
        <li><a href="/websocket">WebSocket Client</a> - Pure WebSocket signaling</li>
        <li><a href="/oak">OAK WebSocket Client</a> - WebSocket with OAK camera support</li>
        <li><a href="/diagnostics">Diagnostics</a> - Server status and connection tests</li>
        <li><a href="/mobile-test">Mobile Test</a> - Quick mobile camera test</li>
    </ul>
    
    <h2>📋 Testing Instructions (Socket.IO):</h2>
    <ol>
        <li><strong>Start P2P Server:</strong> <code>python p2p_webrtc.py</code> (port 4000)</li>
        <li><strong>Start Client Server:</strong> <code>python client_server.py</code> (port 8080)</li>
        <li><strong>Open Multiple Browsers:</strong>
            <ul>
                <li>Browser 1: <a href="http://localhost:4000">http://localhost:4000</a> (Main P2P app)</li>
                <li>Browser 2: <a href="http://localhost:8080/minimal">http://localhost:8080/minimal</a> (Sample client)</li>
            </ul>
        </li>
        <li><strong>Connect:</strong> Both should connect to server at localhost:4000</li>
        <li><strong>Join Room:</strong> Both join the same room name (e.g., "room1")</li>
        <li><strong>Result:</strong> You should see video from both cameras!</li>
    </ol>
    
    <h2>� OAK Camera Testing:</h2>
    <ol>
        <li><strong>Start WebSocket Server:</strong> <code>python websocket_server.py</code> (port 8765)</li>
        <li><strong>Start OAK Bridge:</strong> <code>python oak_camera_bridge.py</code> (port 8766)</li>
        <li><strong>Start HTTP Server:</strong> <code>python client_server.py</code> (port 5001)</li>
        <li><strong>Open OAK Client:</strong> <a href="http://localhost:5001/oak">http://localhost:5001/oak</a></li>
        <li><strong>Connect & Test:</strong> Connect to server → Connect OAK Camera → Join room → Start video</li>
        <li><strong>Multi-Device:</strong> Open same URL on multiple devices for P2P video chat</li>
    </ol>
    
    <h2>�🔗 Testing Instructions (WebSocket):</h2>
    <ol>
        <li><strong>Start Both Servers:</strong> <code>python start_servers.py</code></li>
        <li><strong>Open WebSocket Client:</strong> <a href="http://localhost:8080/websocket">http://localhost:8080/websocket</a></li>
        <li><strong>Connect and Test:</strong> Click "Connect", join a room, start video</li>
        <li><strong>Multi-Device:</strong> Open same URL on multiple devices</li>
    </ol>
    
    <h2>🌐 Multi-Device Testing:</h2>
    <p>Use these URLs on different devices on the same network:</p>
    <ul>
        <li><strong>Socket.IO Server:</strong> http://192.168.1.105:4000</li>
        <li><strong>HTTP Server:</strong> http://192.168.1.105:8080</li>
        <li><strong>WebSocket Server:</strong> ws://192.168.1.105:8765</li>
    </ul>
    
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    '''

if __name__ == '__main__':
    print("🎥 Starting WebRTC HTTP Server...")
    print("📱 Main Client: http://localhost:5001")
    print("🔗 WebSocket Client: http://localhost:5001/websocket")
    print("🔶 OAK Camera Client: http://localhost:5001/oak")
    print("📱 Mobile Client: http://localhost:5001/mobile")
    print("🐛 Debug Client: http://localhost:5001/debug")
    print("📋 Test Instructions: http://localhost:5001/test")
    print("🔧 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
