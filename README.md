# WebRTC P2P Video Chat Server with OAK Camera Support

A professional WebRTC signaling server for peer-to-peer video communication with high-quality OAK camera streaming support and multiple streaming technology options.

## 🔶 OAK Camera Features

- **Professional Quality**: 1280x720 @ 30fps streaming from OAK-D cameras
- **Multiple Streaming Technologies**: WebCodecs, GStreamer, and Canvas options
- **Visual Technology Comparison**: Side-by-side performance analysis
- **WebRTC Integration**: Seamless P2P video chat using OAK camera as source
- **Real-time Streaming**: Low-latency high-quality video for professional applications
- **Browser Compatible**: Works in any modern web browser without plugins

## ⚡ Streaming Technologies

### � WebCodecs
- **Best Performance**: ~2-5ms latency with hardware acceleration
- **Compatibility**: Chrome 94+, Edge 94+
- **Use Case**: When you need the absolute lowest latency

### �🚀 GStreamer (NEW: Real Integration)
- **Real Pipelines**: Actual GStreamer pipelines with `gst-launch-1.0`
- **Hardware Acceleration**: NVENC, VAAPI support when available
- **Graceful Fallback**: Optimized canvas processing if GStreamer unavailable
- **Performance**: ~5-8ms latency with hardware acceleration
- **Compatibility**: Most browsers via WebSocket bridge

### 🎨 Canvas
- **Universal Compatibility**: Works in all browsers
- **Performance**: ~10-20ms latency
- **Use Case**: Maximum compatibility across all devices and browsers

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- OAK-D camera (optional, for high-quality streaming)
- Modern web browser with WebRTC support
- GStreamer (optional, for hardware-accelerated streaming)

### 1. Install Dependencies
```bash
pip install -r requirements.txt

# Optional: Install GStreamer for hardware acceleration
# Ubuntu/Debian:
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good

# macOS:
brew install gstreamer gst-plugins-base gst-plugins-good
```

### 2. Start Complete System (Recommended)
```bash
# Start all servers including GStreamer bridge
python start_comprehensive_servers.py
```

### 3. Legacy Server Setup
```bash
# Start basic OAK servers (without GStreamer)
python start_oak_servers.py
```

### 4. Access the Universal Client
- **🎯 Universal OAK Client**: http://localhost:8000/clients/oak_websocket_client.html
- **Features**: 
  - Technology selection (WebCodecs/GStreamer/Canvas)
  - Visual comparison mode
  - Real-time performance metrics
  - Export comparison reports

## � How to Use WebRTC with OAK Camera

### Step-by-Step Guide:

1. **Open OAK Camera Client**: Navigate to http://localhost:5001/oak

2. **Connect to Signaling Server**: 
   - Click "Connect to Server" button
   - Wait for "Connected to signaling server" status

3. **Connect OAK Camera**:
   - Click "🔶 Connect OAK Camera" button
   - Wait for "Connected (1280x720@30fps)" status

4. **Join a Room**:
   - Enter a room name (e.g., "my-room")
   - Click "Join Room" button

5. **Start Video Streaming**:
   - Click "Start Video" button
   - Your OAK camera feed will appear in the local video area

6. **Connect Peer for Video Chat**:
   - Open the same URL (http://localhost:5001/oak) on another device/browser
   - Follow steps 2-5 with the same room name
   - Both participants will see each other's video streams!

### Alternative: Regular Camera
If you don't have an OAK camera:
1. Click "🔍 Detect Cameras" to find available cameras
2. Select a camera from the dropdown
3. Click "📱 Use Regular Camera"
4. Follow steps 4-6 above

## 🌐 Architecture

```
Browser Client A          Browser Client B
       ↓                         ↓
   HTTP Server (5001)       HTTP Server (5001)
       ↓                         ↓
WebSocket Signaling (8765) ←→ WebSocket Signaling (8765)
       ↓
OAK Camera Bridge (8766)
       ↓
   OAK-D Camera
```

### Server Components:

- **WebSocket Signaling Server** (port 8765): Handles WebRTC signaling between peers
- **OAK Camera Bridge** (port 8766): Streams OAK camera frames to browsers
- **HTTP Client Server** (port 5001): Serves web applications

## 📱 Available Clients

| Client | URL | Description |
|--------|-----|-------------|
| **🔶 OAK Camera** | `/oak` | **Recommended** - Full OAK camera support |
| WebSocket | `/websocket` | Standard WebRTC client |
| Mobile | `/mobile` | Mobile-optimized interface |
| Debug | `/debug` | Detailed logging and diagnostics |
| Minimal | `/minimal` | Simple interface |
| Screenshare | `/screenshare` | Screen sharing demo |

## 🔧 OAK Camera Setup

### Detecting Your OAK Camera
```bash
# Test OAK camera detection
python test_oak_simple.py

# Detailed OAK camera info
python detect_oak_camera.py
```

### Troubleshooting OAK Camera
1. **Camera Not Found**:
   ```bash
   # Check USB connection
   system_profiler SPUSBDataType | grep -i movidius
   ```

2. **Bridge Connection Issues**:
   - Ensure OAK camera bridge is running on port 8766
   - Check for port conflicts: `lsof -i :8766`

3. **Performance Issues**:
   - Close other applications using the camera
   - Use Chrome/Edge for best WebRTC performance

## 🌐 Multi-Device Testing

For testing across multiple devices on the same network:

1. **Find your IP address**:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. **Use your IP instead of localhost**:
   - **OAK Client**: http://192.168.1.xxx:5001/oak
   - **WebSocket Server**: ws://192.168.1.xxx:8765
   - **OAK Bridge**: ws://192.168.1.xxx:8766

Replace `192.168.1.xxx` with your actual IP address.

## 📋 Features

### Core Features
- ✅ Pure WebSocket signaling (no Socket.IO dependency)
- ✅ Room-based peer connections
- ✅ Real-time video/audio chat
- ✅ NAT traversal with STUN servers
- ✅ Mobile-friendly responsive design

### OAK Camera Features
- ✅ **High-Quality Streaming**: 1280x720 @ 30fps
- ✅ **Professional Camera**: Superior image quality vs standard webcams
- ✅ **Seamless Integration**: Drop-in replacement for regular cameras
- ✅ **Auto Detection**: Automatic OAK camera discovery
- ✅ **Fallback Support**: Use regular cameras when OAK not available

## 🛠 Development

### Technology Stack
- **Backend**: Python with `websockets`, `Flask`, and `depthai`
- **Frontend**: Vanilla JavaScript with WebRTC APIs
- **Signaling**: Pure WebSocket protocol
- **Camera**: DepthAI for OAK camera integration

### OAK Camera Integration
The OAK camera integration works by:
1. **Camera Bridge**: Captures frames from OAK camera using DepthAI
2. **WebSocket Streaming**: Sends JPEG frames to browser clients
3. **Canvas Integration**: Converts frames to MediaStream for WebRTC
4. **P2P Transmission**: WebRTC handles peer-to-peer video transmission

## 📁 Project Structure

```
webrtc-server/
├── websocket_server.py           # WebSocket signaling server
├── client_server.py             # HTTP server for clients
├── oak_camera_bridge.py         # OAK camera WebSocket bridge
├── start_oak_servers.py         # Start all servers script
├── test_oak_simple.py           # OAK camera detection test
├── detect_oak_camera.py         # Detailed OAK camera detection
├── clients/                     # HTML client applications
│   ├── oak_websocket_client.html  # OAK camera client (main)
│   ├── websocket_client.html      # Standard WebRTC client
│   ├── mobile_client.html         # Mobile-optimized client
│   ├── debug_client.html          # Debug client
│   └── ...                        # Other clients
├── requirements.txt             # Python dependencies
├── README.md                   # This file
└── OAK_CAMERA_README.md        # Detailed OAK camera guide
```

## 🎯 Use Cases

### Professional Applications
- **High-Quality Video Conferencing**: Professional-grade camera quality
- **Remote Collaboration**: Clear video for detailed work discussions
- **Education/Training**: High-quality streaming for instructional content
- **Telemedicine**: Professional camera quality for medical consultations

### Development & Testing
- **WebRTC Development**: Test WebRTC applications with high-quality video
- **Camera Integration**: Prototype applications using professional cameras
- **Multi-Device Testing**: Test across different devices and networks

## 🔍 Example Workflow

### Basic WebRTC Chat
```bash
# 1. Start servers
python start_oak_servers.py

# 2. Open in browser (Person A)
# http://localhost:5001/oak

# 3. Open in another browser/device (Person B)  
# http://localhost:5001/oak

# 4. Both join same room → Video chat!
```

### OAK Camera Streaming
```bash
# 1. Connect OAK camera via USB
# 2. Start servers: python start_oak_servers.py
# 3. Open: http://localhost:5001/oak
# 4. Click: Connect to Server → Connect OAK Camera → Join Room → Start Video
# 5. Share URL with others for high-quality video chat!
```

---

**🎉 Start building professional video applications with OAK camera support!**

For detailed OAK camera setup and troubleshooting, see [OAK_CAMERA_README.md](OAK_CAMERA_README.md).