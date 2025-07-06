# WebRTC with OAK Camera Support

This project enables high-quality P2P video streaming using OAK (OpenCV AI Kit) cameras through WebRTC in the browser.

## 🔶 OAK Camera Features

- **High Quality**: 1280x720 @ 30fps streaming from OAK-D camera
- **WebRTC Integration**: Seamless P2P video chat using OAK camera as source
- **Browser Compatible**: Works in any modern web browser
- **Real-time**: Low-latency streaming for interactive video calls

## 🚀 Quick Start

### 1. Start All Servers
```bash
python start_oak_servers.py
```

### 2. Open OAK Camera Client
Navigate to: http://localhost:5001/oak

### 3. Test the Setup
1. Click "Connect to Server"
2. Click "🔶 Connect OAK Camera" 
3. Enter a room name and click "Join Room"
4. Click "Start Video"
5. Open the same URL on another device for P2P video chat!

## 🛠️ Manual Setup

If you prefer to start servers individually:

### Start WebSocket Signaling Server
```bash
python websocket_server.py
# Runs on ws://localhost:8765
```

### Start OAK Camera Bridge
```bash
python oak_camera_bridge.py  
# Runs on ws://localhost:8766
```

### Start Web Client Server
```bash
python client_server.py
# Runs on http://localhost:5001
```

## 📱 Available Clients

- **OAK Camera Client**: http://localhost:5001/oak
- **Regular WebSocket Client**: http://localhost:5001/websocket
- **Mobile Client**: http://localhost:5001/mobile
- **Debug Client**: http://localhost:5001/debug

## 🔧 Troubleshooting

### OAK Camera Not Found
1. Ensure OAK-D camera is connected via USB
2. Check device detection:
   ```bash
   python test_oak_simple.py
   ```
3. Verify USB connection:
   ```bash
   system_profiler SPUSBDataType | grep -i movidius
   ```

### WebSocket Connection Issues
- Ensure all servers are running
- Check firewall settings
- Try different browser

### Performance Issues
- Close other applications using camera
- Use Chrome/Edge for best WebRTC performance
- Ensure stable network connection

## 🌐 Multi-Device Testing

For testing across multiple devices on the same network, use your computer's IP address:

- **OAK Client**: http://192.168.1.105:5001/oak
- **WebSocket Server**: ws://192.168.1.105:8765
- **OAK Bridge**: ws://192.168.1.105:8766

Replace `192.168.1.105` with your actual IP address.

## 📋 Architecture

```
Browser (Client A)     Browser (Client B)
       ↓                        ↓
   HTTP Server (5001)    HTTP Server (5001)
       ↓                        ↓
WebSocket Signaling (8765) ← → WebSocket Signaling (8765)
       ↓                        
OAK Camera Bridge (8766)
       ↓
   OAK-D Camera
```

## 🔶 OAK Camera Specifications

- **Resolution**: 1280x720 (720p)
- **Frame Rate**: 30 FPS
- **Quality**: High-quality RGB camera with excellent low-light performance
- **Connection**: USB 3.0 for reliable high-bandwidth streaming

## 🎯 Use Cases

- **High-Quality Video Conferencing**: Professional-grade camera quality
- **Remote Collaboration**: Clear video for detailed work
- **Education/Training**: High-quality streaming for instructional content
- **Surveillance/Monitoring**: Professional camera capabilities in browser
