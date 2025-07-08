# Docker Deployment Guide

This guide explains how to run the WebRTC OAK Camera Server using Docker.

## 🚀 Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the container
docker compose up --build

# Run in background
docker compose up -d --build

# View logs
docker compose logs -f webrtc-oak-server
```

### 2. Build and Run with Docker

```bash
# Build the image
docker build -t webrtc-oak-server .

# Run the container
docker run -d \
  --name webrtc-oak-server \
  -p 8000:8000 \
  -p 8765:8765 \
  -p 8766:8766 \
  -p 8767:8767 \
  --device=/dev/bus/usb \
  -v $(pwd)/logs:/app/logs \
  webrtc-oak-server
```

## 🔶 OAK Camera Support

### With OAK Camera Hardware

For the best OAK camera support in Docker, use this command:

```bash
# Recommended: Full USB access for OAK cameras
docker run -d \
  --name webrtc-oak-server \
  --privileged \
  -v /dev:/dev \
  -p 8000:8000 \
  -p 8765:8765 \
  -p 8766:8766 \
  -p 8767:8767 \
  webrtc-oak-server

# Alternative: Specific device access
docker compose up --build

# Or with docker run:
docker run -d \
  --name webrtc-oak-server \
  -p 8000:8000 \
  -p 8765:8765 \
  -p 8766:8766 \
  -p 8767:8767 \
  --privileged \
  --device=/dev/bus/usb \
  -v /dev/bus/usb:/dev/bus/usb \
  webrtc-oak-server
```

**Note**: If you see "Process oak_bridge exited with code 0" repeatedly, your OAK camera is not accessible in the container. Try the privileged mode command above.

### Without OAK Camera (Software Only)

```bash
# Run without hardware access (uses fallback cameras)
docker run -d \
  --name webrtc-oak-server \
  -p 8000:8000 \
  -p 8765:8765 \
  -p 8767:8767 \
  webrtc-oak-server
```

## 🌐 Access Points

Once running, access the application at:

- **Main Client**: http://localhost:8000/clients/oak_websocket_client.html
- **Legacy OAK Client**: http://localhost:8000/oak
- **WebSocket Signaling**: ws://localhost:8765
- **OAK Camera Bridge**: ws://localhost:8766
- **GStreamer Bridge**: ws://localhost:8767

## 🔧 Configuration

### Environment Variables

You can customize the container with environment variables:

```bash
docker run -d \
  --name webrtc-oak-server \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  -e LOG_LEVEL=DEBUG \
  webrtc-oak-server
```

### Volume Mounts

- `/app/logs`: Application logs
- `/dev/bus/usb`: USB device access for OAK cameras

## 🚀 Production Deployment

### With Nginx Reverse Proxy

```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d --build

# Access via nginx on port 80
# http://localhost/clients/oak_websocket_client.html
```

### SSL/HTTPS Setup

1. Place your SSL certificates in `docker/ssl/`:
   ```
   docker/ssl/
   ├── cert.pem
   └── key.pem
   ```

2. Uncomment the HTTPS server block in `docker/nginx.conf`

3. Update the HTTP server to redirect to HTTPS

## 🔍 Troubleshooting

### Check Container Status

```bash
# View running containers
docker-compose ps

# Check logs
docker-compose logs webrtc-oak-server

# Access container shell
docker exec -it webrtc-oak-server /bin/bash
```

### Common Issues

1. **OAK Camera Not Detected / Bridge Keeps Exiting**
   ```bash
   # Check if OAK camera is detected on HOST first
   lsusb | grep -i movidius
   
   # Check USB device access in container
   docker exec webrtc-oak-server lsusb
   docker exec webrtc-oak-server ls -la /dev/bus/usb/
   
   # Verify privileged mode is enabled
   # Make sure --privileged flag is used OR use --device=/dev/bus/usb
   
   # Try running with full USB access:
   docker run -d \
     --name webrtc-oak-server \
     --privileged \
     -v /dev:/dev \
     -p 8000:8000 -p 8765:8765 -p 8766:8766 -p 8767:8767 \
     webrtc-oak-server
   ```

2. **OAK Bridge Process Exiting with Code 0**
   ```bash
   # This usually means the OAK camera is not accessible
   # Check container logs for OAK camera detection:
   docker compose logs webrtc-oak-server | grep -i oak
   
   # Access container and test OAK camera directly:
   docker exec -it webrtc-oak-server /bin/bash
   python -c "import depthai as dai; print('Devices:', dai.Device.getAllAvailableDevices())"
   ```

2. **GStreamer Not Working**
   ```bash
   # Check GStreamer installation
   docker exec webrtc-oak-server gst-launch-1.0 --version
   ```

3. **Port Conflicts**
   ```bash
   # Check if ports are already in use
   netstat -tulpn | grep :8000
   
   # Use different ports
   docker run -p 9000:8000 ... webrtc-oak-server
   ```

## 🛠️ Development

### Development with Volume Mounts

```bash
# Mount source code for development
docker run -d \
  --name webrtc-dev \
  -p 8000:8000 \
  -p 8765:8765 \
  -p 8766:8766 \
  -p 8767:8767 \
  -v $(pwd):/app \
  --device=/dev/bus/usb \
  webrtc-oak-server
```

### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose down
docker-compose up --build
```

## 📊 Monitoring

### Health Check

```bash
# Check container health
docker inspect webrtc-oak-server | grep -A 10 "Health"

# Manual health check
curl -f http://localhost:8000/clients/oak_websocket_client.html
```

### Resource Usage

```bash
# Monitor resource usage
docker stats webrtc-oak-server

# Check disk usage
docker system df
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi webrtc-oak-server

# Clean up everything
docker system prune -a
```
