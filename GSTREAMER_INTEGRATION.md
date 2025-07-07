# GStreamer Integration Documentation

## Overview

This document clarifies the actual GStreamer integration in the WebRTC-OAK camera system and explains the differences between real GStreamer usage and optimized canvas fallbacks.

## Streaming Technology Options

### 1. WebCodecs 🔥
- **What it is**: Browser-native hardware-accelerated video encoding/decoding
- **Performance**: Excellent (~2-5ms latency)
- **Compatibility**: Chrome 94+, Edge 94+
- **Implementation**: Uses `VideoEncoder`/`VideoDecoder` APIs directly

### 2. GStreamer 🚀 (NEW: Real Integration)
- **What it is**: Industry-standard multimedia framework with actual pipeline support
- **Performance**: Good (~5-8ms latency with hardware acceleration)
- **Compatibility**: Most browsers (via WebSocket bridge)
- **Implementation**: **Actual GStreamer pipelines** using `gst-launch-1.0`

#### GStreamer Implementation Details

The GStreamer option now includes:

1. **Real GStreamer Bridge** (`gstreamer_bridge.py`):
   - Checks for GStreamer availability on the system
   - Launches actual `gst-launch-1.0` pipelines
   - Supports multiple pipeline configurations:
     - `basic`: Simple OAK to WebRTC with x264 encoding
     - `optimized`: Hardware-accelerated encoding (NVENC if available)
     - `websocket`: Direct WebSocket streaming with JPEG compression

2. **Fallback Mechanism**:
   - If GStreamer bridge is unavailable → Falls back to optimized canvas
   - If GStreamer is not installed → Falls back to optimized canvas
   - If pipeline fails to start → Falls back to optimized canvas

3. **Actual GStreamer Pipelines**:
   ```bash
   # Basic pipeline
   gst-launch-1.0 v4l2src device=/dev/video0 ! \
     video/x-raw,width=1280,height=720,framerate=30/1 ! \
     videoconvert ! x264enc tune=zerolatency bitrate=2000 ! \
     rtph264pay ! udpsink host=127.0.0.1 port=5000

   # Hardware accelerated pipeline
   gst-launch-1.0 v4l2src device=/dev/video0 ! \
     video/x-raw,width=1280,height=720,framerate=30/1 ! \
     videoconvert ! queue max-size-buffers=2 ! \
     nvh264enc preset=low-latency-hq bitrate=3000 ! \
     h264parse ! rtph264pay ! udpsink host=127.0.0.1 port=5000
   ```

### 3. Canvas 🎨
- **What it is**: Universal browser-compatible canvas-based rendering
- **Performance**: Basic (~10-20ms latency)
- **Compatibility**: All browsers
- **Implementation**: Standard Canvas 2D API with frame capture

## How to Use Real GStreamer

### Prerequisites

1. **Install GStreamer**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base \
     gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
     gstreamer1.0-plugins-ugly

   # macOS (via Homebrew)
   brew install gstreamer gst-plugins-base gst-plugins-good \
     gst-plugins-bad gst-plugins-ugly

   # Verify installation
   gst-launch-1.0 --version
   ```

2. **Hardware Acceleration** (optional but recommended):
   ```bash
   # NVIDIA hardware acceleration
   sudo apt install gstreamer1.0-plugins-nvidia

   # Intel hardware acceleration  
   sudo apt install gstreamer1.0-vaapi
   ```

### Starting the Complete System

1. **Start all servers** (includes GStreamer bridge):
   ```bash
   python start_comprehensive_servers.py
   ```

2. **Or start individual components**:
   ```bash
   # Start GStreamer bridge separately
   python gstreamer_bridge.py

   # Start other servers
   python start_oak_servers.py
   ```

### Using GStreamer in the Client

1. Open the client: `http://localhost:8000/clients/oak_websocket_client.html`
2. Connect to OAK camera
3. Select "🚀 GStreamer" streaming technology
4. The system will:
   - Try to connect to GStreamer bridge (port 8767)
   - Check if GStreamer is available on the system
   - Start appropriate GStreamer pipeline
   - Fall back to optimized canvas if any step fails

## Visual Comparison Mode

The comparison mode now accurately shows:
- **WebCodecs**: True hardware acceleration when supported
- **GStreamer**: Real GStreamer pipelines when available, fallback when not
- **Canvas**: Standard canvas processing

Each panel displays:
- Real-time FPS and latency metrics
- Technology status (real vs fallback)
- Performance advantages and trade-offs

## Troubleshooting

### GStreamer Not Working

1. **Check if GStreamer is installed**:
   ```bash
   gst-launch-1.0 --version
   ```

2. **Check GStreamer bridge connection**:
   - Open browser developer tools
   - Look for "Connected to GStreamer bridge" in console
   - Check WebSocket connection to `ws://localhost:8767`

3. **Check pipeline compatibility**:
   - Some pipelines require specific hardware
   - NVIDIA pipelines need NVENC support
   - V4L2 pipelines need compatible video devices

### Fallback Behavior

The system is designed to gracefully fall back:
```
GStreamer Selection → GStreamer Bridge → Real Pipeline → Success
                  ↓                   ↓               ↓
              Bridge Failed    GStreamer Missing  Pipeline Failed
                  ↓                   ↓               ↓
              Optimized Canvas ← Optimized Canvas ← Optimized Canvas
```

## Performance Comparison

| Technology | Latency | CPU Usage | GPU Usage | Compatibility |
|------------|---------|-----------|-----------|---------------|
| WebCodecs  | 2-5ms   | Low       | High      | Chrome only   |
| GStreamer  | 5-8ms   | Medium    | Medium    | Most browsers |
| Canvas     | 10-20ms | High      | Low       | All browsers  |

## Implementation Status

✅ **Completed**:
- Real GStreamer bridge with actual pipeline support
- Multiple pipeline configurations (basic, optimized, websocket)
- Graceful fallback mechanisms
- System requirement checking
- Process monitoring and management

🔧 **Clarified**:
- GStreamer option now uses real GStreamer when available
- Clear distinction between real pipelines and fallback processing
- Comprehensive documentation of what each option actually does
- Visual comparison mode accurately reflects true vs fallback behavior

📋 **Future Enhancements**:
- Custom pipeline configuration UI
- Real-time pipeline switching
- Advanced hardware acceleration detection
- Pipeline performance profiling
