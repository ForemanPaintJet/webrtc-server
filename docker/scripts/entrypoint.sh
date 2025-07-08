#!/bin/bash
set -e

echo "🐳 Starting WebRTC OAK Camera Server Container..."

# Check if GStreamer is available
echo "🔧 Checking GStreamer installation..."
if command -v gst-launch-1.0 >/dev/null 2>&1; then
    echo "✅ GStreamer available: $(gst-launch-1.0 --version | head -n1)"
else
    echo "⚠️  GStreamer not found, fallback mode will be used"
fi

# Check for OAK camera access (if running with device access)
echo "🔶 Checking for OAK camera access..."
if ls /dev/bus/usb/ >/dev/null 2>&1; then
    echo "✅ USB device access available"

    # List all USB devices for debugging
    echo "📋 Available USB devices:"
    lsusb 2>/dev/null || echo "   lsusb command not available"

    # Check specifically for OAK cameras (Movidius devices)
    if lsusb 2>/dev/null | grep -i movidius; then
        echo "🎯 OAK camera detected!"
    else
        echo "🔶 No OAK cameras detected"
        echo "   Make sure your OAK camera is connected and recognized by the host"
        echo "   On host, check with: lsusb | grep -i movidius"
    fi

    # Check USB device permissions
    echo "🔒 Checking USB device permissions..."
    ls -la /dev/bus/usb/ | head -5

else
    echo "⚠️  No USB device access - OAK cameras will not be available"
    echo "   To enable OAK cameras, run with: docker run --device=/dev/bus/usb"
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
python -c "import websockets; print('✅ websockets available')" || echo "❌ websockets not available"
python -c "import depthai; print('✅ depthai available')" || echo "❌ depthai not available"
python -c "import cv2; print('✅ opencv available')" || echo "❌ opencv not available"
python -c "import flask; print('✅ flask available')" || echo "❌ flask not available"

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Set permissions for log files
chmod 755 /app/logs

# Export environment variables for the application
export PYTHONPATH="/app:$PYTHONPATH"

echo "🚀 Starting WebRTC servers..."
echo "📱 Client will be available at: http://localhost:8000/clients/oak_websocket_client.html"
echo "🔧 Signaling server: ws://localhost:8765"
echo "🔶 OAK camera bridge: ws://localhost:8766"
echo "🎬 GStreamer bridge: ws://localhost:8767"

# Execute the command passed to the container
exec "$@"
