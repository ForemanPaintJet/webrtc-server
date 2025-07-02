# WebRTC Browser Camera Projects

Two different WebRTC implementations for different use cases.

## 🎯 Projects Available

### 1. 📷 Simple Camera (`simple_camera.py`)
**Local camera capture only - no P2P connections**
```bash
python simple_camera.py
# Access: http://localhost:3000
```
- ✅ Basic camera capture using WebRTC
- ✅ Start/stop controls
- ✅ Simple, educational code

### 2. 🔗 P2P Video Chat (`p2p_webrtc.py`) 
**Full WebRTC P2P implementation with signaling server**
```bash
python p2p_webrtc.py
# Access: http://localhost:4000
```
- ✅ **Peer-to-peer video calls**
- ✅ **Signaling server** (Socket.IO)
- ✅ **Room-based chat**
- ✅ **Real-time communication**

## 🚀 Quick Start

### For P2P Video Chat:
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start P2P server:**
   ```bash
   python p2p_webrtc.py
   ```

3. **Open two browser tabs:**
   - Tab 1: http://localhost:4000
   - Tab 2: http://localhost:4000

4. **Test P2P connection:**
   - Both tabs: Start Camera → Join Room "room1"
   - You should see each other's video!

## 🔧 P2P WebRTC Architecture

### Components:

1. **Signaling Server** (Flask-SocketIO)
   - Handles room management
   - Exchanges WebRTC offers/answers
   - Manages ICE candidates
   - User presence and room state

2. **WebRTC Peer Connection**
   - Direct browser-to-browser video/audio
   - Uses STUN servers for NAT traversal
   - Encrypted peer-to-peer communication

3. **Camera Capture**
   - `getUserMedia()` for local camera access
   - MediaStream management
   - Video element display

### Signaling Flow:
```
User A                 Signaling Server                User B
  |                           |                          |
  |-- Join Room ------------->|                          |
  |                           |<-- Join Room ------------|
  |                           |-- User Joined ---------->|
  |<-- User Joined -----------|                          |
  |                           |                          |
  |-- Offer ----------------->|                          |
  |                           |-- Offer ---------------->|
  |                           |<-- Answer ---------------|
  |<-- Answer -----------------|                          |
  |                           |                          |
  |-- ICE Candidates -------->|-- ICE Candidates ------->|
  |<-- ICE Candidates ---------|<-- ICE Candidates -------|
  |                           |                          |
  |<=== Direct P2P Video =========================>|
```

## 🎥 Features Comparison

| Feature | Simple Camera | P2P Video Chat |
|---------|---------------|----------------|
| Camera Capture | ✅ | ✅ |
| Local Video | ✅ | ✅ |
| Remote Video | ❌ | ✅ |
| Signaling Server | ❌ | ✅ |
| P2P Connection | ❌ | ✅ |
| Rooms | ❌ | ✅ |
| Multi-user | ❌ | ✅ |

## 🌐 How to Test P2P

1. **Same Computer**: Open two browser tabs
2. **Different Computers**: Use the IP address shown in terminal
3. **Different Networks**: Requires STUN/TURN servers (included)

### Example Multi-device Test:
- Device 1: http://192.168.1.105:4000
- Device 2: http://192.168.1.105:4000
- Both join same room name

## 🔒 Security Features

- **STUN servers** for NAT traversal
- **Encrypted P2P** communication  
- **User permissions** required for camera
- **Room-based** isolation
- **No video data** passes through server

## 📋 Requirements

```bash
Flask==2.3.2           # Web server
Flask-SocketIO==5.3.4  # Real-time signaling
```

## 🛠️ Customization

### Add TURN Server (for better connectivity):
```javascript
const configuration = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        {
            urls: 'turn:your-turn-server.com:3478',
            username: 'username',
            credential: 'password'
        }
    ]
};
```

### Change Video Quality:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({
    video: { width: 1280, height: 720 },  // HD
    audio: true
});
```

---

**🎉 Now you have both simple camera capture AND full P2P video chat!**

- **Learning**: Start with `simple_camera.py`
- **Production**: Use `p2p_webrtc.py` for real video chat
