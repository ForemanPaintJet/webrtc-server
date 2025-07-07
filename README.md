# WebRTC P2P Video Chat Se## 🚀 Recent Updatesver wit### 🚀 GStreamer (Real Integration) OAK Camera Support

A professional WebRTC signaling server for peer-to-peer video communication with high-quality OAK camera streaming support, real GStreamer hardware acceleration, and multiple streaming technology options.

## 📋 Table of Contents# 📋 Table of Con## 🚀 Recent UpdatesentsRTC### 🚀 GStreamer (Real Integration)P2P Video Chat Server with OAK Camera Support

A professional WebRTC signaling server for peer-to-peer video communication with high-quality OAK camera streaming support, real GStreamer hardware acceleration, and multiple streaming technology options.

## � Table of Contents

- [Recent Updates](#-recent-updates)
- [OAK Camera Features](#-oak-camera-features)
- [Streaming Technologies](#️-streaming-technologies)
- [Quick Start](#-quick-start)
- [How to Use WebRTC with OAK Camera](#-how-to-use-webrtc-with-oak-camera)
- [Architecture](#-architecture)
- [Available Clients](#-available-clients)
- [GStreamer Setup & Troubleshooting](#-gstreamer-setup--troubleshooting)
- [OAK Camera Setup](#-oak-camera-setup)
- [Multi-Device Testing](#-multi-device-testing)
- [Features](#-features)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Use Cases](#-use-cases)
- [Example Workflow](#-example-workflow)

## �🚀 Recent Updates

### 🚀 GStreamer (Hardware Accelerated)
- **Real GStreamer Integration**: Actual `gst-launch-1.0` pipelines with hardware acceleration
- **Hardware Support**: NVENC (NVIDIA), VAAPI (Intel), VideoToolbox (macOS)
- **Automatic Installation Detection**: Clear instructions for macOS and Ubuntu
- **Graceful Fallback**: Optimized canvas processing if GStreamer unavailable
- **Performance**: ~5-8ms latency with hardware acceleration
- **Status Indicators**: Real-time status showing "Real GStreamer ✅" or "Fallback Mode ⚠️"
- **Compatibility**: All browsers via WebSocket bridge

## 🔶 OAK Camera Features

- **Professional Quality**: 1280x720 @ 30fps streaming from OAK-D cameras
- **Multiple Streaming Technologies**: WebCodecs, GStreamer, and Canvas options
- **Visual Technology Comparison**: Side-by-side performance analysis
- **WebRTC Integration**: Seamless P2P video chat using OAK camera as source
- **Real-time Streaming**: Low-latency high-quality video for professional applications
- **Browser Compatible**: Works in any modern web browser without plugins

## ⚡ Streaming Technologies

### 🚀 WebCodecs
- **Best Performance**: ~2-5ms latency with hardware acceleration
- **Compatibility**: Chrome 94+, Edge 94+
- **Use Case**: When you need the absolute lowest latency

### � GStreamer (Real Integration)
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
- **GStreamer** (recommended, for hardware-accelerated streaming)

### 1. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install GStreamer for hardware acceleration (RECOMMENDED)
# macOS (using Homebrew):
brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad

# Ubuntu/Debian:
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad

# Verify GStreamer installation:
gst-launch-1.0 --version
```

### 2. Start the Complete System (RECOMMENDED)
```bash
# Start all servers with GStreamer support
python start_comprehensive_servers.py

# You should see:
# ✅ GStreamer available: gst-launch-1.0 version X.X.X
# ✅ All servers started successfully!
```

### 3. Access the Enhanced Client
- **🎯 Universal OAK Client**: http://localhost:8000/clients/oak_websocket_client.html
- **Features**: 
  - Technology selection with real-time status indicators
  - Visual comparison mode for performance analysis
  - Real-time performance metrics and FPS monitoring
  - Export detailed comparison reports
  - Hardware acceleration detection and status

## 📹 How to Use WebRTC with OAK Camera

### Step-by-Step Guide:

1. **Open OAK Camera Client**: Navigate to http://localhost:8000/clients/oak_websocket_client.html

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
   - Open the same URL (http://localhost:8000/clients/oak_websocket_client.html) on another device/browser
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
   HTTP Server (8000)       HTTP Server (8000)
       ↓                         ↓
WebSocket Signaling (8765) ←→ WebSocket Signaling (8765)
       ↓                         ↓
OAK Camera Bridge (8766)    GStreamer Bridge (8767)
       ↓                         ↓
   OAK-D Camera           Hardware Acceleration
```

### Server Components:

- **WebSocket Signaling Server** (port 8765): Handles WebRTC signaling between peers
- **OAK Camera Bridge** (port 8766): Streams OAK camera frames to browsers
- **GStreamer Bridge** (port 8767): Hardware-accelerated video processing with fallback
- **HTTP Client Server** (port 8000): Serves enhanced web applications

## 📱 Available Clients

| Client | URL | Description |
|--------|-----|-------------|
| **🔶 Enhanced OAK Client** | `/clients/oak_websocket_client.html` | **Recommended** - Full OAK + GStreamer support |
| Legacy OAK | `/oak` | Basic OAK camera support |
| WebSocket | `/websocket` | Standard WebRTC client |
| Mobile | `/mobile` | Mobile-optimized interface |
| Debug | `/debug` | Detailed logging and diagnostics |
| Minimal | `/minimal` | Simple interface |
| Screenshare | `/screenshare` | Screen sharing demo |

## 🔧 GStreamer Setup & Troubleshooting

### Installing GStreamer

**macOS (Homebrew):**
```bash
brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad
```

**Ubuntu/Debian:**
```bash
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

**Verify Installation:**
```bash
gst-launch-1.0 --version
# Should output: gst-launch-1.0 version 1.x.x
```

### GStreamer Status Indicators

In the client, look for the GStreamer button status:
- **"Real GStreamer ✅"**: Hardware acceleration available and working
- **"Fallback Mode ⚠️"**: GStreamer not installed, using optimized canvas
- **"Bridge Offline ❌"**: Cannot connect to GStreamer bridge server
- **"Checking..."**: Detecting GStreamer availability

### Troubleshooting GStreamer
1. **"Fallback Mode" showing**:
   ```bash
   # Check if GStreamer is installed
   which gst-launch-1.0
   
   # Reinstall if needed
   brew reinstall gstreamer  # macOS
   # or
   sudo apt reinstall gstreamer1.0-tools  # Ubuntu
   ```

2. **Bridge connection issues**:
   - Ensure comprehensive servers are running: `python start_comprehensive_servers.py`
   - Check for port conflicts: `lsof -i :8767`

3. **Performance issues**:
   - Verify hardware acceleration is working
   - Check system resources and close other video applications

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
   - **Enhanced Client**: http://192.168.1.xxx:8000/clients/oak_websocket_client.html
   - **WebSocket Server**: ws://192.168.1.xxx:8765
   - **OAK Bridge**: ws://192.168.1.xxx:8766
   - **GStreamer Bridge**: ws://192.168.1.xxx:8767

Replace `192.168.1.xxx` with your actual IP address.

## 📋 Features

### Core Features
- ✅ Pure WebSocket signaling (no Socket.IO dependency)
- ✅ Room-based peer connections
- ✅ Real-time video/audio chat
- ✅ NAT traversal with STUN servers
- ✅ Mobile-friendly responsive design
- ✅ **Real GStreamer Integration**: Hardware-accelerated video processing
- ✅ **Automatic Fallback**: Graceful degradation when hardware unavailable
- ✅ **Real-time Status**: Live indicators for all system components

### OAK Camera Features
- ✅ **High-Quality Streaming**: 1280x720 @ 30fps
- ✅ **Professional Camera**: Superior image quality vs standard webcams
- ✅ **Seamless Integration**: Drop-in replacement for regular cameras
- ✅ **Auto Detection**: Automatic OAK camera discovery
- ✅ **Fallback Support**: Use regular cameras when OAK not available

### GStreamer Features
- ✅ **Hardware Acceleration**: NVENC, VAAPI, VideoToolbox support
- ✅ **Real-time Detection**: Automatic GStreamer capability detection
- ✅ **Performance Monitoring**: Live FPS and latency metrics
- ✅ **Visual Comparison**: Side-by-side technology performance analysis
- ✅ **Installation Guidance**: Clear setup instructions with status feedback

## 🛠 Development

### Technology Stack
- **Backend**: Python with `websockets`, `depthai`, and GStreamer integration
- **Frontend**: Vanilla JavaScript with WebRTC APIs and hardware acceleration detection
- **Signaling**: Pure WebSocket protocol
- **Camera**: DepthAI for OAK camera integration
- **Video Processing**: GStreamer pipelines with hardware acceleration support

### Enhanced Integration
The system now provides multiple video processing paths:
1. **OAK Camera Bridge**: Captures frames from OAK camera using DepthAI
2. **GStreamer Bridge**: Hardware-accelerated video processing with real pipelines
3. **WebSocket Streaming**: Sends processed frames to browser clients
4. **Technology Selection**: Choose between WebCodecs, GStreamer, or Canvas
5. **Automatic Fallback**: Seamless degradation when hardware unavailable
6. **Performance Monitoring**: Real-time metrics and comparison tools

## 📁 Project Structure

```
webrtc-server/
├── websocket_server.py                    # WebSocket signaling server
├── oak_camera_bridge.py                   # OAK camera WebSocket bridge
├── gstreamer_bridge.py                    # GStreamer hardware acceleration bridge
├── start_comprehensive_servers.py         # Start all servers (RECOMMENDED)
├── start_oak_servers.py                   # Legacy server startup
├── clients/                               # HTML client applications
│   ├── oak_websocket_client.html         # Enhanced OAK + GStreamer client (MAIN)
│   ├── websocket_client.html             # Standard WebRTC client
│   ├── mobile_client.html                # Mobile-optimized client
│   ├── debug_client.html                 # Debug client
│   └── ...                               # Other clients
├── requirements.txt                       # Python dependencies
├── README.md                             # This file
├── GSTREAMER_INSTALLATION_GUIDE.md      # Detailed GStreamer setup guide
└── OAK_CAMERA_README.md                 # Detailed OAK camera guide
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

### Enhanced WebRTC Chat with Hardware Acceleration
```bash
# 1. Start comprehensive servers
python start_comprehensive_servers.py

# 2. Open enhanced client (Person A)
# http://localhost:8000/clients/oak_websocket_client.html

# 3. Open in another browser/device (Person B)  
# http://localhost:8000/clients/oak_websocket_client.html

# 4. Select streaming technology and join same room → Hardware-accelerated video chat!
```

### OAK Camera with GStreamer Streaming
```bash
# 1. Connect OAK camera via USB
# 2. Ensure GStreamer is installed: gst-launch-1.0 --version
# 3. Start servers: python start_comprehensive_servers.py
# 4. Open: http://localhost:8000/clients/oak_websocket_client.html
# 5. Check GStreamer status shows "Real GStreamer ✅"
# 6. Connect OAK Camera → Select GStreamer → Join Room → Start Video
# 7. Share URL with others for professional-quality hardware-accelerated video chat!
```

---

**🎉 Start building professional video applications with real hardware acceleration!**

For detailed setup guides, see:
- [GSTREAMER_INSTALLATION_GUIDE.md](GSTREAMER_INSTALLATION_GUIDE.md) - Complete GStreamer setup and troubleshooting
- [OAK_CAMERA_README.md](OAK_CAMERA_README.md) - Detailed OAK camera setup and usage