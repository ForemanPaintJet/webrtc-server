# WebRTC Client Samples Guide

This directory contains multiple WebRTC client samples that demonstrate different use cases and approaches for connecting to your WebRTC signaling server with OAK camera support.

## 🚀 Quick Start

1. **Start the comprehensive WebRTC system:**
   ```bash
   python start_comprehensive_servers.py
   ```

2. **Access the enhanced client:**
   - **🎯 Main Enhanced Client**: http://localhost:8000/clients/oak_websocket_client.html

3. **Or access legacy clients:**
   - Legacy OAK Client: http://localhost:5001/oak
   - Standard clients: http://localhost:5001/ (various options)

## 📱 Available Clients

### 1. 🎯 Enhanced OAK Client (RECOMMENDED)
**URL:** http://localhost:8000/clients/oak_websocket_client.html

The most advanced client with full OAK camera support.

**Features:**
- OAK camera integration with 1280x720@30fps
- Technology selection (WebCodecs/Canvas)
- Real-time status indicators
- Performance comparison tools
- Automatic fallback handling
- Easy-to-read code structure
- Perfect for learning WebRTC fundamentals

**Best for:** Beginners, code examples, simple implementations

---

### 2. 📱 Mobile Client
**URL:** http://localhost:5002/client/mobile

Optimized for mobile devices with touch-friendly interface.

**Features:**
- Mobile-responsive design
- Touch-optimized controls
- Camera switching (front/back)
- Orientation change handling
- Emoji-rich interface

**Best for:** Mobile testing, smartphone/tablet usage

---

### 3. 🔍 Debug Client
**URL:** http://localhost:5002/client/debug

Advanced debugging and monitoring features for development.

**Features:**
- Real-time connection statistics
- Detailed event logging
- ICE candidate tracking
- Performance monitoring
- Connection state visualization
- Log download functionality

**Best for:** Development, troubleshooting, performance analysis

---

### 4. 🖥️ Screen Share Client
**URL:** http://localhost:5002/client/screenshare

Specialized for screen sharing and streaming applications.

**Features:**
- Screen sharing capability
- Camera streaming
- Source switching (screen/camera)
- Recording functionality
- Participant management
- High-quality video support

**Best for:** Presentations, demos, screen sharing sessions

---

### 5. 🎨 Original Sample Client
**URL:** http://localhost:5002/client/original

The original full-featured client with beautiful design.

**Features:**
- Beautiful gradient UI
- Complete feature set
- Connection management
- Status indicators
- Professional appearance

**Best for:** Production use, demonstrations

## 🔧 Testing Different Scenarios

### Single Device Testing
1. Open two different clients in separate browser tabs
2. Use different room names to test multiple rooms
3. Use the same room name to test peer-to-peer connection

### Multi-Device Testing
1. Connect devices to the same WiFi network
2. Replace `localhost` with your computer's IP address in the server URL
3. Open clients on different devices using the network IP

### Example Multi-Device Setup:
- Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Update server URL to: `http://YOUR_IP:5001`
- Access clients at: `http://YOUR_IP:5002/`

## 🌐 Network Testing

### Local Network (WiFi)
```
Server URL: http://192.168.1.100:5001
Client URL: http://192.168.1.100:5002
```

### Public Access (with port forwarding)
```
Server URL: http://YOUR_PUBLIC_IP:5001
Client URL: http://YOUR_PUBLIC_IP:5002
```

## 📋 Testing Checklist

### Basic Functionality
- [ ] Camera/microphone access granted
- [ ] Local video appears
- [ ] Successfully connects to server
- [ ] Joins room without errors
- [ ] Remote video appears when second user joins
- [ ] Audio/video quality is acceptable

### Advanced Features (depending on client)
- [ ] Mute/unmute audio
- [ ] Enable/disable video
- [ ] Screen sharing works
- [ ] Camera switching (mobile)
- [ ] Connection statistics update (debug client)
- [ ] Recording functionality (screen share client)

### Network Scenarios
- [ ] Same device, different browser tabs
- [ ] Different devices, same WiFi
- [ ] Different networks (if public access configured)
- [ ] Mobile devices
- [ ] Various browsers (Chrome, Firefox, Safari, Edge)

## 🐛 Troubleshooting

### Common Issues

**"Could not load Socket.IO"**
- Make sure `p2p_webrtc.py` is running on port 5001
- Check that the server URL is correct

**"Camera access denied"**
- Grant camera/microphone permissions in browser
- Use HTTPS for some browsers (not needed for localhost)

**"Connection failed"**
- Verify server is running and accessible
- Check firewall settings
- Ensure ports 5001 and 5002 are available

**No remote video**
- Check that both users are in the same room
- Verify network connectivity between devices
- Check browser developer console for errors

### Debug Tools

1. **Browser Developer Console:**
   - Press F12 to open developer tools
   - Check Console tab for errors
   - Check Network tab for failed requests

2. **Debug Client:**
   - Use the debug client for detailed connection logs
   - Monitor real-time statistics
   - Download logs for analysis

3. **Server Logs:**
   - Check terminal running `p2p_webrtc.py` for server-side logs
   - Look for connection and room events

## 🔧 Customization

### Adding New Clients
1. Create a new HTML file in the `clients/` directory
2. Add entry to `clients_server.py` in the `client_files` dictionary
3. Update the main index page template

### Modifying Existing Clients
- Edit HTML files directly in the `clients/` directory
- Restart `clients_server.py` to see changes
- Use browser refresh to reload client

### Server Configuration
- Modify server URLs in client HTML files
- Update port numbers if needed
- Add authentication or room restrictions

## 📚 Learning Resources

### Code Structure
- Each client demonstrates different WebRTC patterns
- Compare implementations to understand trade-offs
- Use minimal client as a starting point for new projects

### WebRTC Concepts Demonstrated
- Media stream acquisition (`getUserMedia`, `getDisplayMedia`)
- Peer connection establishment
- Signaling via Socket.IO
- ICE candidate exchange
- STUN server usage

### Next Steps
- Implement TURN server for NAT traversal
- Add data channels for chat
- Implement recording and playback
- Add video filters and effects
- Create mobile apps using WebRTC

## 🤝 Contributing

Feel free to create new client samples or improve existing ones:
1. Follow the existing code patterns
2. Include comprehensive error handling
3. Add helpful user feedback
4. Test on multiple devices and browsers
5. Update this documentation

---

*Happy WebRTC testing! 🎥*
