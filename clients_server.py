from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_DIR = os.path.join(BASE_DIR, 'clients')

@app.route('/')
def index():
    """Main page with links to all client samples"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebRTC Client Samples</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 3em;
        }
        
        .header p {
            margin: 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .clients-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .client-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .client-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border-color: rgba(255,255,255,0.3);
            color: white;
            text-decoration: none;
        }
        
        .client-card h3 {
            margin: 0 0 15px 0;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .client-card p {
            margin: 0 0 15px 0;
            opacity: 0.9;
            line-height: 1.5;
        }
        
        .features {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .features li {
            margin: 5px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .features li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #4caf50;
            font-weight: bold;
        }
        
        .server-info {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            text-align: center;
        }
        
        .server-info h3 {
            margin: 0 0 15px 0;
        }
        
        .server-url {
            background: rgba(0,0,0,0.2);
            padding: 10px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 1.1em;
            margin: 10px 0;
        }
        
        .warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.5);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .warning-icon {
            font-size: 1.2em;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎥 WebRTC Client Samples</h1>
            <p>Choose a client to test WebRTC video chat functionality</p>
        </div>
        
        <div class="warning">
            <span class="warning-icon">⚠️</span>
            <strong>Before using these clients:</strong> Make sure your WebRTC signaling server is running on 
            <code>localhost:5001</code>. Run <code>python p2p_webrtc.py</code> in your terminal.
        </div>
        
        <div class="clients-grid">
            <a href="/client/minimal" class="client-card">
                <h3>🎯 Minimal Client</h3>
                <p>Simple, clean interface for basic WebRTC video chat functionality.</p>
                <ul class="features">
                    <li>Basic video calling</li>
                    <li>Simple UI</li>
                    <li>Easy to understand code</li>
                    <li>Perfect for beginners</li>
                </ul>
            </a>
            
            <a href="/client/mobile" class="client-card">
                <h3>📱 Mobile Client</h3>
                <p>Optimized for mobile devices with touch-friendly controls.</p>
                <ul class="features">
                    <li>Mobile-responsive design</li>
                    <li>Touch controls</li>
                    <li>Camera switching</li>
                    <li>Orientation handling</li>
                </ul>
            </a>
            
            <a href="/client/debug" class="client-card">
                <h3>🔍 Debug Client</h3>
                <p>Advanced debugging features for development and troubleshooting.</p>
                <ul class="features">
                    <li>Real-time connection stats</li>
                    <li>Detailed logging</li>
                    <li>ICE candidate tracking</li>
                    <li>Performance monitoring</li>
                </ul>
            </a>
            
            <a href="/client/screenshare" class="client-card">
                <h3>🖥️ Screen Share Client</h3>
                <p>Share your screen or camera with advanced streaming features.</p>
                <ul class="features">
                    <li>Screen sharing</li>
                    <li>Camera streaming</li>
                    <li>Recording capability</li>
                    <li>Participant management</li>
                </ul>
            </a>
            
            <a href="/client/original" class="client-card">
                <h3>🎨 Original Sample</h3>
                <p>The original feature-rich client with beautiful UI design.</p>
                <ul class="features">
                    <li>Beautiful gradient design</li>
                    <li>Full feature set</li>
                    <li>Connection management</li>
                    <li>Status indicators</li>
                </ul>
            </a>
        </div>
        
        <div class="server-info">
            <h3>🔗 Server Information</h3>
            <p>All clients connect to your WebRTC signaling server:</p>
            <div class="server-url">http://localhost:5001</div>
            <p>Make sure to start the server with: <code>python p2p_webrtc.py</code></p>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/client/<client_name>')
def serve_client(client_name):
    """Serve individual client HTML files"""
    client_files = {
        'minimal': 'minimal_client.html',
        'mobile': 'mobile_client.html', 
        'debug': 'debug_client.html',
        'screenshare': 'screenshare_client.html',
        'original': '../client_sample.html'  # Original client is in parent directory
    }
    
    if client_name not in client_files:
        return "Client not found", 404
    
    file_path = client_files[client_name]
    
    # Handle original client which is in parent directory
    if client_name == 'original':
        return send_from_directory(BASE_DIR, 'client_sample.html')
    else:
        return send_from_directory(CLIENTS_DIR, file_path)

# Serve socket.io.js for clients
@app.route('/socket.io/socket.io.js')
def socket_io_js():
    """Proxy socket.io.js from the main server"""
    try:
        import requests
        response = requests.get('http://localhost:5001/socket.io/socket.io.js')
        return response.content, 200, {'Content-Type': 'application/javascript'}
    except:
        return '''
        // Socket.IO fallback - please make sure your WebRTC server is running on localhost:5001
        console.error("Could not load Socket.IO from main server. Please ensure p2p_webrtc.py is running on localhost:5001");
        ''', 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    print("🎥 WebRTC Client Sample Server")
    print("=" * 40)
    print("📂 Available clients:")
    print("   • Minimal Client: http://localhost:5002/client/minimal")
    print("   • Mobile Client:  http://localhost:5002/client/mobile")
    print("   • Debug Client:   http://localhost:5002/client/debug")
    print("   • Screen Share:   http://localhost:5002/client/screenshare")
    print("   • Original:       http://localhost:5002/client/original")
    print()
    print("🌐 Main index page: http://localhost:5002/")
    print()
    print("⚠️  IMPORTANT: Make sure your WebRTC signaling server is running:")
    print("   python p2p_webrtc.py")
    print()
    print("🚀 Starting client server on port 5002...")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
