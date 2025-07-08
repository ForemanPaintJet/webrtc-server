# Docker Configuration

This directory contains all Docker-related files organized for easy management and deployment.

## 📁 Directory Structure

```
docker/
├── README.md              # This file - Docker organization guide
├── compose/               # Docker Compose configurations
│   ├── docker-compose.yml     # Production Docker Compose
│   └── docker-compose.dev.yml # Development Docker Compose
├── config/                # Configuration files
│   ├── nginx.conf             # Nginx reverse proxy configuration
│   └── oak-camera.rules       # udev rules for OAK camera access
├── scripts/               # Docker-related scripts
│   ├── entrypoint.sh          # Container entrypoint script
│   └── build-and-test.sh      # Build and test automation
├── tests/                 # Docker test utilities
│   ├── test_docker_deps.py    # Test Docker dependencies
│   └── test_oak_docker.py     # Test OAK camera in Docker
└── docs/                  # Docker documentation
    └── DOCKER.md              # Comprehensive Docker guide
```

## 🚀 Quick Start

### Production Deployment
```bash
# From project root
docker compose -f docker/compose/docker-compose.yml up -d
```

### Development Environment
```bash
# From project root
docker compose -f docker/compose/docker-compose.dev.yml up
```

### Build and Test
```bash
# Run automated build and test
./docker/scripts/build-and-test.sh
```

## 🔧 Configuration Files

### `config/nginx.conf`
- Nginx reverse proxy configuration
- Routes WebSocket connections
- Serves static client files
- Handles CORS and security headers

### `config/oak-camera.rules`
- udev rules for OAK camera permissions
- Enables non-root access to OAK devices
- Must be installed on host system for Docker access

## 📋 Scripts

### `scripts/entrypoint.sh`
- Container initialization script
- Sets up udev rules
- Configures permissions
- Starts services

### `scripts/build-and-test.sh`
- Automated build and test pipeline
- Builds Docker image
- Runs dependency tests
- Tests OAK camera access

## 🧪 Testing

### Test Docker Dependencies
```bash
python docker/tests/test_docker_deps.py
```

### Test OAK Camera Access
```bash
python docker/tests/test_oak_docker.py
```

### Test in Docker Container
```bash
docker run --rm -it \
  --device=/dev/bus/usb \
  webrtc-oak-server \
  python docker/tests/test_oak_docker.py
```

## 📖 Documentation

For comprehensive Docker usage, troubleshooting, and deployment guides, see:
- [`docs/DOCKER.md`](docs/DOCKER.md) - Complete Docker documentation

## 🔗 Integration

This Docker setup integrates with:
- **OAK Camera Bridge** - Hardware camera access
- **GStreamer Pipeline** - Video processing
- **WebRTC Signaling** - Real-time communication
- **WebSocket Servers** - Client connections

## 🌐 Network Architecture

```
Client Browser ←→ Nginx (80/443) ←→ Python Services
                    ↓
                WebSocket Connections:
                - 8765: WebRTC Signaling
                - 8766: OAK Camera Bridge
                - 8767: GStreamer Bridge
```

## 🔧 Customization

### Override Compose Settings
Create `docker-compose.override.yml` in the compose directory:
```yaml
version: '3.8'
services:
  webrtc-server:
    ports:
      - "8080:80"  # Custom port mapping
    environment:
      - DEBUG=true
```

### Custom Configuration
- Mount custom configs: `-v ./my-config:/app/config`
- Override entrypoint: `--entrypoint=/custom/script.sh`
- Add environment variables in compose files

## 🏗️ Building

### Standard Build
```bash
docker build -t webrtc-oak-server .
```

### Multi-platform Build
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t webrtc-oak-server .
```

### Development Build
```bash
docker build -f Dockerfile.dev -t webrtc-oak-server:dev .
```

## 🚨 Troubleshooting

Common issues and solutions:

### OAK Camera Not Detected
1. Check host detection: `lsusb | grep -i movidius`
2. Install udev rules: `sudo cp docker/config/oak-camera.rules /etc/udev/rules.d/`
3. Run with privileged access: `--privileged -v /dev:/dev`

### Port Conflicts
1. Check running containers: `docker ps`
2. Stop conflicting services: `sudo systemctl stop nginx`
3. Use different ports in compose files

### Permission Issues
1. Check container user: `docker exec -it container_name whoami`
2. Fix ownership: `docker exec -it container_name chown -R appuser:appuser /app`
3. Use proper udev rules for device access

## 📝 Notes

- All paths in scripts are relative to project root
- Docker Compose files expect to be run from project root
- Configuration files are copied into container during build
- Test scripts can be run both on host and in container
