# WebRTC P2P Video Chat Server with OAK Camera Support

A professional WebRTC signaling server for peer-to-peer video communication with high-quality OAK camera streaming support and multiple streaming technology options.

## 📋 Table of Contents

- [Docker Deployment](#-quick-start)
- [Recent Updates](#-recent-updates)
- [OAK Camera Features](#-oak-camera-features)
- [Streaming Technologies](#️-streaming-technologies)
- [Quick Start](#-quick-start)
- [How to Use WebRTC with OAK Camera](#-how-to-use-webrtc-with-oak-camera)
- [Architecture](#-architecture)
- [Available Clients](#-available-clients)
- [OAK Camera Setup](#-oak-camera-setup)
- [Multi-Device Testing](#-multi-device-testing)
- [Features](#-features)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Use Cases](#-use-cases)
- [Example Workflow](#-example-workflow)
- [Platform Limitations](#-platform-limitations)

## 🚀 Recent Updates

### 🚀 WebCodecs & Canvas Streaming Technologies
- **WebCodecs Integration**: Hardware-accelerated streaming with ~2-5ms latency
- **Canvas Fallback**: Universal compatibility across all browsers
- **Performance Optimizations**: Enhanced streaming quality and reduced latency
- **Simplified Architecture**: Streamlined codebase without external dependencies
- **Status Indicators**: Real-time performance monitoring
- **Cross-browser Compatibility**: Works seamlessly across all modern browsers

## 🔶 OAK Camera Features

- **Professional Quality**: 1280x720 @ 30fps streaming from OAK-D cameras
- **Multiple Streaming Technologies**: WebCodecs and Canvas options
- **Visual Technology Comparison**: Side-by-side performance analysis
- **WebRTC Integration**: Seamless P2P video chat using OAK camera as source
- **Real-time Streaming**: Low-latency high-quality video for professional applications
- **Browser Compatible**: Works in any modern web browser without plugins

## ⚡ Streaming Technologies

### 🚀 WebCodecs
- **Best Performance**: ~2-5ms latency with hardware acceleration
- **Compatibility**: Chrome 94+, Edge 94+
- **Use Case**: When you need the absolute lowest latency

### 🎨 Canvas
- **Universal Compatibility**: Works in all browsers
- **Performance**: ~10-20ms latency
- **Use Case**: Maximum compatibility across all devices and browsers

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ OR Docker
- OAK-D camera (optional, for high-quality streaming)
- Modern web browser with WebRTC support

### Option 1: Docker Deployment (RECOMMENDED)

**⚠️ Important Note for macOS Users:**
Docker containers on macOS cannot access USB devices (including cameras) due to macOS kernel limitations. This affects:
- Regular webcam streaming between clients
- OAK camera access from within containers

**macOS Docker Workarounds:**
1. **For OAK Camera**: Run the OAK camera bridge natively on the host:
   ```bash
   # Terminal 1: Run servers in Docker
   ./docker-start.sh build
   
   # Terminal 2: Run OAK bridge natively on host
   python oak_camera_bridge.py
   ```

2. **For Regular Webcams**: Use native Python installation instead of Docker on macOS
3. **For Linux/Windows**: Full Docker support including USB camera access

```bash
# Quick start with convenience script
./docker-start.sh build

# Or manually with Docker Compose
docker compose -f docker/compose/docker-compose.yml up --build

# Development environment with live reload
./docker-start.sh dev

# Access the application at:
# http://localhost:8000/clients/oak_websocket_client.html
```

**Docker Commands:**
- `./docker-start.sh build` - Quick production setup
- `./docker-start.sh dev` - Development with live reload  
- `./docker-start.sh test` - Run build and test suite
- `./docker-start.sh logs` - Monitor application logs
- `./docker-start.sh stop` - Stop all services

For detailed Docker instructions, see [docker/docs/DOCKER.md](docker/docs/DOCKER.md).

### Option 2: Native Python Installation

### 1. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Start the Complete System (RECOMMENDED)
```bash
# Start all servers
python start_comprehensive_servers.py

# You should see:
# ✅ All servers started successfully!
```

### 3. Access the Enhanced Client
- **🎯 Universal OAK Client**: http://localhost:8000/clients/oak_websocket_client.html
- **Features**: 
  - Technology selection with real-time status indicators
  - Visual comparison mode for performance analysis
  - Real-time performance metrics and FPS monitoring
  - Export detailed comparison reports

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
OAK Camera Bridge (8766)    Video File Bridge (8768)
       ↓                         ↓
   OAK-D Camera           Video File Streaming
```

### Server Components:

- **WebSocket Signaling Server** (port 8765): Handles WebRTC signaling between peers
- **OAK Camera Bridge** (port 8766): Streams OAK camera frames to browsers
- **Video File Bridge** (port 8768): Streams video files to browsers
- **HTTP Client Server** (port 8000): Serves enhanced web applications

## 📱 Available Clients

| Client | URL | Description |
|--------|-----|-------------|
| **🔶 Enhanced OAK Client** | `/clients/oak_websocket_client.html` | **Recommended** - Full OAK camera support |
| Legacy OAK | `/oak` | Basic OAK camera support |
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
   - **Enhanced Client**: http://192.168.1.xxx:8000/clients/oak_websocket_client.html
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
- ✅ **WebCodecs & Canvas Integration**: Hardware-accelerated video processing
- ✅ **Automatic Fallback**: Graceful degradation between technologies
- ✅ **Real-time Status**: Live indicators for all system components

### OAK Camera Features
- ✅ **High-Quality Streaming**: 1280x720 @ 30fps
- ✅ **Professional Camera**: Superior image quality vs standard webcams
- ✅ **Seamless Integration**: Drop-in replacement for regular cameras
- ✅ **Auto Detection**: Automatic OAK camera discovery
- ✅ **Fallback Support**: Use regular cameras when OAK not available

### Streaming Technology Features
- ✅ **WebCodecs Acceleration**: Hardware-accelerated video processing
- ✅ **Real-time Detection**: Automatic capability detection
- ✅ **Performance Monitoring**: Live FPS and latency metrics
- ✅ **Visual Comparison**: Side-by-side technology performance analysis
- ✅ **Cross-browser Support**: Universal compatibility

## 🛠 Development

### Technology Stack
- **Backend**: Python with `websockets` and `depthai`
- **Frontend**: Vanilla JavaScript with WebRTC APIs and hardware acceleration detection
- **Signaling**: Pure WebSocket protocol
- **Camera**: DepthAI for OAK camera integration
- **Video Processing**: WebCodecs and Canvas with hardware acceleration support

### Enhanced Integration
The system now provides multiple video processing paths:
1. **OAK Camera Bridge**: Captures frames from OAK camera using DepthAI
2. **Video File Bridge**: Streams video files for testing and demos
3. **WebSocket Streaming**: Sends processed frames to browser clients
4. **Technology Selection**: Choose between WebCodecs or Canvas
5. **Automatic Fallback**: Seamless degradation between technologies
6. **Performance Monitoring**: Real-time metrics and comparison tools

## 📁 Project Structure

```
webrtc-server/
├── websocket_server.py                    # WebSocket signaling server
├── oak_camera_bridge.py                   # OAK camera WebSocket bridge
├── video_file_bridge.py                   # Video file streaming bridge
├── start_comprehensive_servers.py         # Start all servers (RECOMMENDED)
├── start_oak_servers.py                   # Legacy server startup
├── clients/                               # HTML client applications
│   ├── oak_websocket_client.html         # Enhanced OAK camera client (MAIN)
│   ├── websocket_client.html             # Standard WebRTC client
│   ├── mobile_client.html                # Mobile-optimized client
│   ├── debug_client.html                 # Debug client
│   └── ...                               # Other clients
├── requirements.txt                       # Python dependencies
├── README.md                             # This file
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

### OAK Camera with WebCodecs Streaming
```bash
# 1. Connect OAK camera via USB
# 2. Start servers: python start_comprehensive_servers.py
# 3. Open: http://localhost:8000/clients/oak_websocket_client.html
# 4. Connect OAK Camera → Select WebCodecs → Join Room → Start Video
# 5. Share URL with others for professional-quality hardware-accelerated video chat!
```

---

## 🚨 Platform Limitations

### macOS Docker USB Camera Restrictions

Docker containers on macOS **cannot access USB devices** (including cameras) due to macOS kernel limitations. This affects:

- **Regular webcam streaming**: Won't work from Docker containers
- **OAK camera access**: Cannot access OAK-D devices from containers

**Solutions for macOS**:
1. **Hybrid approach**: Run main services in Docker, camera bridge natively
2. **Native installation**: Use Python directly for full camera support
3. **See detailed guide**: [PLATFORM_LIMITATIONS.md](PLATFORM_LIMITATIONS.md)

### Cross-Platform Support

| Platform | Docker USB Support | Recommended Approach |
|----------|-------------------|---------------------|
| **macOS** | ❌ No USB access | Native Python or hybrid |
| **Linux** | ✅ Full support | Docker (preferred) |  
| **Windows** | ✅ With WSL2 | Docker with WSL2 |

For detailed platform-specific instructions and workarounds, see **[PLATFORM_LIMITATIONS.md](PLATFORM_LIMITATIONS.md)**.

---

**🎉 Start building professional video applications with real hardware acceleration!**

For detailed setup guides, see:
- [OAK_CAMERA_README.md](OAK_CAMERA_README.md) - Detailed OAK camera setup and usage