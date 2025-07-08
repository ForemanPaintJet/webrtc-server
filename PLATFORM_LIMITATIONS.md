# Platform Limitations and Workarounds

This document outlines platform-specific limitations and their workarounds for the WebRTC OAK Camera Server.

## 🍎 macOS Limitations

### Docker USB Device Access

**Issue**: Docker Desktop on macOS cannot access USB devices due to macOS kernel architecture.

**Affected Functionality**:
- Regular webcam access from within containers
- OAK camera access from within containers  
- Any USB-connected cameras or devices
- Audio device access (microphones, speakers)

**Root Cause**: 
macOS runs Docker in a Linux VM (HyperKit), and USB devices cannot be passed through to the VM due to macOS security and kernel limitations.

**Workarounds**:

1. **Hybrid Approach (Recommended for OAK cameras)**:
   ```bash
   # Terminal 1: Run main services in Docker
   ./docker-start.sh build
   
   # Terminal 2: Run camera bridge natively on host
   python oak_camera_bridge.py
   ```

2. **Native Python Installation**:
   ```bash
   # Install dependencies natively
   pip install -r requirements.txt
   
   # Run all services natively
   python start_comprehensive_servers.py
   ```

3. **Development Workflow**:
   ```bash
   # Use Docker for development without cameras
   ./docker-start.sh dev
   
   # Test camera functionality natively when needed
   python test_oak_simple.py
   ```

### Browser Camera Access

**Issue**: Regular webcam streaming between clients doesn't work when servers run in Docker.

**Solution**: Use native Python installation for webcam testing on macOS.

## 🐧 Linux Limitations

### USB Device Permissions

**Issue**: USB devices may not be accessible due to permission restrictions.

**Solutions**:

1. **Grant USB access to Docker**:
   ```bash
   # Add user to dialout group
   sudo usermod -a -G dialout $USER
   
   # Run with privileged access
   docker run --privileged --device=/dev/bus/usb
   ```

2. **Set up udev rules**:
   ```bash
   # Copy provided udev rules
   sudo cp docker/config/oak-camera.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

## 🪟 Windows Limitations

### Docker Desktop Requirements

**Issue**: USB device access requires specific Docker Desktop configuration.

**Requirements**:
- Docker Desktop for Windows with WSL2 backend
- Windows 10/11 with WSL2 enabled
- Proper USB device drivers installed

**Solutions**:

1. **Enable WSL2 integration**:
   - Docker Desktop → Settings → Resources → WSL Integration
   - Enable integration with your WSL2 distro

2. **USB device pass-through**:
   ```bash
   # Run with device access
   docker run --privileged -v /dev:/dev
   ```

## 🔧 General Docker Limitations

### Performance Considerations

**Issue**: Container overhead can impact real-time video processing.

**Solutions**:
- Use `--cpus` to allocate sufficient CPU resources
- Consider native installation for production deployments
- Use hardware acceleration when available

### Network Configuration

**Issue**: WebRTC requires specific network configuration for optimal performance.

**Solutions**:
- Use host networking for development: `--network host`
- Configure proper port forwarding for production
- Ensure STUN/TURN servers are accessible

## 🚀 Recommended Platform Setup

### Development

| Platform | Recommended Approach |
|----------|---------------------|
| macOS | Native Python installation |
| Linux | Docker with USB device access |
| Windows | Docker Desktop with WSL2 |

### Production

| Platform | Recommended Approach |
|----------|---------------------|
| macOS | Native Python with process manager |
| Linux | Docker with orchestration (K8s/Docker Swarm) |
| Windows | Docker or native with Windows Service |

## 🔍 Testing USB Device Access

### Quick Test Script

```bash
# Test USB device visibility in container
docker run --rm -it --privileged -v /dev:/dev python:3.9 python3 -c "
import os
print('USB devices in container:')
try:
    devices = os.listdir('/dev/bus/usb')
    for bus in devices:
        bus_path = f'/dev/bus/usb/{bus}'
        if os.path.isdir(bus_path):
            devices = os.listdir(bus_path)
            print(f'  Bus {bus}: {len(devices)} devices')
except Exception as e:
    print(f'  Error accessing USB: {e}')
"
```

### OAK Camera Test

```bash
# Test OAK camera detection
docker run --rm -it --privileged -v /dev:/dev \
  luxonis/depthai:latest python3 -c "
import depthai as dai
devices = dai.Device.getAllAvailableDevices()
print(f'OAK devices found: {len(devices)}')
for device in devices:
    print(f'  {device.getMxId()} - {device.name}')
"
```

## 📚 Additional Resources

- [Docker Desktop macOS Known Issues](https://docs.docker.com/desktop/troubleshoot/known-issues/#known-issues-for-mac)
- [OAK Camera Docker Setup](https://docs.luxonis.com/en/latest/pages/tutorials/docker/)
- [WebRTC Docker Deployment Best Practices](https://webrtc.org/getting-started/remote-streams)

## 🤝 Contributing

If you discover additional platform limitations or workarounds, please:

1. Test the workaround thoroughly
2. Document the exact steps
3. Submit a pull request with updates to this file
4. Include platform and version information
