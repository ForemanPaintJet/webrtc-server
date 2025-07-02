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
    """Serve the sample client HTML file"""
    return send_file('client_sample.html')

@app.route('/test')
def test_info():
    """Test endpoint with connection instructions"""
    return '''
    <h1>🎥 WebRTC Client Test Server</h1>
    <p><strong>Main Client:</strong> <a href="/">http://localhost:5001</a></p>
    <p><strong>P2P Server:</strong> <a href="http://localhost:4000">http://localhost:4000</a></p>
    
    <h2>📋 Testing Instructions:</h2>
    <ol>
        <li><strong>Start P2P Server:</strong> <code>python p2p_webrtc.py</code> (port 4000)</li>
        <li><strong>Start Client Server:</strong> <code>python client_server.py</code> (port 5001)</li>
        <li><strong>Open Multiple Browsers:</strong>
            <ul>
                <li>Browser 1: <a href="http://localhost:4000">http://localhost:4000</a> (Main P2P app)</li>
                <li>Browser 2: <a href="http://localhost:5001">http://localhost:5001</a> (Sample client)</li>
            </ul>
        </li>
        <li><strong>Connect:</strong> Both should connect to server at localhost:4000</li>
        <li><strong>Join Room:</strong> Both join the same room name (e.g., "room1")</li>
        <li><strong>Result:</strong> You should see video from both cameras!</li>
    </ol>
    
    <h2>🌐 Multi-Device Testing:</h2>
    <p>Use these URLs on different devices on the same network:</p>
    <ul>
        <li><strong>P2P Server:</strong> http://192.168.1.105:4000</li>
        <li><strong>Client:</strong> http://192.168.1.105:5001</li>
    </ul>
    
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    '''

if __name__ == '__main__':
    if not os.path.exists('client_sample.html'):
        print("❌ Error: client_sample.html not found!")
        print("Make sure you're running this from the correct directory.")
        exit(1)
    
    print("🎥 Starting WebRTC Client Test Server...")
    print("📱 Sample Client: http://localhost:5001")
    print("📋 Test Instructions: http://localhost:5001/test")
    print("🔧 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
