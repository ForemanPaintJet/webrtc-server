from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'webrtc-p2p-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active rooms and users
rooms = {}
users = {}

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P2P WebRTC Video Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .video-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        video {
            width: 100%;
            height: 300px;
            background: #000;
            border-radius: 10px;
            object-fit: cover;
        }
        
        .controls {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
        }
        
        .room-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        input, button {
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }
        
        input {
            flex: 1;
            min-width: 200px;
            color: #333;
        }
        
        button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        button:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #f44336, #d32f2f);
        }
        
        .status {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .log {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
            .room-controls {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎥 P2P WebRTC Video Chat</h1>
        <p>Real-time peer-to-peer video communication with signaling server</p>
    </div>
    
    <div class="controls">
        <h3>📱 Room Controls</h3>
        <div class="room-controls">
            <input type="text" id="roomInput" placeholder="Enter room name (e.g., 'meeting1')" value="room1">
            <button id="joinBtn" onclick="joinRoom()">Join Room</button>
            <button id="leaveBtn" onclick="leaveRoom()" disabled>Leave Room</button>
        </div>
        
        <div class="room-controls">
            <button id="startCameraBtn" onclick="startCamera()">Start Camera</button>
            <button id="stopCameraBtn" onclick="stopCamera()" disabled>Stop Camera</button>
        </div>
    </div>
    
    <div class="container">
        <div class="video-section">
            <h3>📹 Your Camera</h3>
            <video id="localVideo" autoplay muted playsinline></video>
        </div>
        
        <div class="video-section">
            <h3>👥 Remote Peer</h3>
            <video id="remoteVideo" autoplay playsinline></video>
        </div>
    </div>
    
    <div class="status">
        <h3>📊 Connection Status</h3>
        <p><strong>Room:</strong> <span id="currentRoom">Not connected</span></p>
        <p><strong>Status:</strong> <span id="connectionStatus">Disconnected</span></p>
        <p><strong>Peers:</strong> <span id="peerCount">0</span></p>
    </div>
    
    <div class="log" id="log"></div>
    
    <script src="/socket.io/socket.io.js"></script>
    <script>
        // WebRTC P2P Implementation
        const localVideo = document.getElementById('localVideo');
        const remoteVideo = document.getElementById('remoteVideo');
        const roomInput = document.getElementById('roomInput');
        const joinBtn = document.getElementById('joinBtn');
        const leaveBtn = document.getElementById('leaveBtn');
        const startCameraBtn = document.getElementById('startCameraBtn');
        const stopCameraBtn = document.getElementById('stopCameraBtn');
        const currentRoom = document.getElementById('currentRoom');
        const connectionStatus = document.getElementById('connectionStatus');
        const peerCount = document.getElementById('peerCount');
        const logDiv = document.getElementById('log');
        
        let socket;
        let localStream;
        let peerConnection;
        let room = null;
        
        // STUN servers for NAT traversal
        const configuration = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
        
        function log(message) {
            console.log(message);
            const timestamp = new Date().toLocaleTimeString();
            logDiv.innerHTML += `<div>${timestamp}: ${message}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }
        
        function updateStatus(status) {
            connectionStatus.textContent = status;
            log(`Status: ${status}`);
        }
        
        // Initialize Socket.IO
        function initSocket() {
            socket = io();
            
            socket.on('connect', () => {
                log('Connected to signaling server');
                updateStatus('Connected to server');
            });
            
            socket.on('disconnect', () => {
                log('Disconnected from signaling server');
                updateStatus('Disconnected');
            });
            
            socket.on('room_joined', (data) => {
                log(`Joined room: ${data.room} (${data.users} users)`);
                room = data.room;
                currentRoom.textContent = room;
                peerCount.textContent = data.users;
                joinBtn.disabled = true;
                leaveBtn.disabled = false;
            });
            
            socket.on('room_left', () => {
                log('Left room');
                room = null;
                currentRoom.textContent = 'Not connected';
                peerCount.textContent = '0';
                joinBtn.disabled = false;
                leaveBtn.disabled = true;
                if (peerConnection) {
                    peerConnection.close();
                    peerConnection = null;
                }
                remoteVideo.srcObject = null;
            });
            
            socket.on('user_joined', (data) => {
                log(`User joined: ${data.user_id}`);
                peerCount.textContent = data.users;
                if (localStream) {
                    createOffer();
                }
            });
            
            socket.on('user_left', (data) => {
                log(`User left: ${data.user_id}`);
                peerCount.textContent = data.users;
                if (peerConnection) {
                    peerConnection.close();
                    peerConnection = null;
                }
                remoteVideo.srcObject = null;
            });
            
            socket.on('offer', async (data) => {
                log('Received offer');
                await handleOffer(data);
            });
            
            socket.on('answer', async (data) => {
                log('Received answer');
                await handleAnswer(data);
            });
            
            socket.on('ice_candidate', async (data) => {
                log('Received ICE candidate');
                await handleIceCandidate(data);
            });
        }
        
        // Start camera
        async function startCamera() {
            try {
                updateStatus('Starting camera...');
                localStream = await navigator.mediaDevices.getUserMedia({
                    video: { width: 640, height: 480 },
                    audio: true
                });
                
                localVideo.srcObject = localStream;
                startCameraBtn.disabled = true;
                stopCameraBtn.disabled = false;
                updateStatus('Camera started');
                log('Camera started successfully');
                
            } catch (error) {
                log('Camera error: ' + error.message);
                updateStatus('Camera error');
            }
        }
        
        // Stop camera
        function stopCamera() {
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
                localStream = null;
                localVideo.srcObject = null;
            }
            startCameraBtn.disabled = false;
            stopCameraBtn.disabled = true;
            updateStatus('Camera stopped');
            log('Camera stopped');
        }
        
        // Join room
        function joinRoom() {
            const roomName = roomInput.value.trim();
            if (!roomName) {
                alert('Please enter a room name');
                return;
            }
            
            log(`Joining room: ${roomName}`);
            socket.emit('join_room', { room: roomName });
        }
        
        // Leave room
        function leaveRoom() {
            if (room) {
                log(`Leaving room: ${room}`);
                socket.emit('leave_room', { room: room });
            }
        }
        
        // Create peer connection
        function createPeerConnection() {
            peerConnection = new RTCPeerConnection(configuration);
            
            // Add local stream
            if (localStream) {
                localStream.getTracks().forEach(track => {
                    peerConnection.addTrack(track, localStream);
                });
            }
            
            // Handle remote stream
            peerConnection.ontrack = (event) => {
                log('Received remote stream');
                remoteVideo.srcObject = event.streams[0];
                updateStatus('Connected to peer');
            };
            
            // Handle ICE candidates
            peerConnection.onicecandidate = (event) => {
                if (event.candidate) {
                    log('Sending ICE candidate');
                    socket.emit('ice_candidate', {
                        room: room,
                        candidate: event.candidate
                    });
                }
            };
            
            // Connection state changes
            peerConnection.onconnectionstatechange = () => {
                log(`Connection state: ${peerConnection.connectionState}`);
                updateStatus(`Peer connection: ${peerConnection.connectionState}`);
            };
        }
        
        // Create offer (caller)
        async function createOffer() {
            createPeerConnection();
            
            try {
                const offer = await peerConnection.createOffer();
                await peerConnection.setLocalDescription(offer);
                
                log('Sending offer');
                socket.emit('offer', {
                    room: room,
                    offer: offer
                });
            } catch (error) {
                log('Error creating offer: ' + error.message);
            }
        }
        
        // Handle offer (callee)
        async function handleOffer(data) {
            createPeerConnection();
            
            try {
                await peerConnection.setRemoteDescription(data.offer);
                
                const answer = await peerConnection.createAnswer();
                await peerConnection.setLocalDescription(answer);
                
                log('Sending answer');
                socket.emit('answer', {
                    room: room,
                    answer: answer
                });
            } catch (error) {
                log('Error handling offer: ' + error.message);
            }
        }
        
        // Handle answer (caller)
        async function handleAnswer(data) {
            try {
                await peerConnection.setRemoteDescription(data.answer);
                log('Answer processed');
            } catch (error) {
                log('Error handling answer: ' + error.message);
            }
        }
        
        // Handle ICE candidate
        async function handleIceCandidate(data) {
            try {
                if (peerConnection) {
                    await peerConnection.addIceCandidate(data.candidate);
                    log('ICE candidate added');
                }
            } catch (error) {
                log('Error adding ICE candidate: ' + error.message);
            }
        }
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (peerConnection) {
                peerConnection.close();
            }
            if (socket) {
                socket.disconnect();
            }
        });
        
        // Initialize
        initSocket();
        log('P2P WebRTC client initialized');
        updateStatus('Ready');
    </script>
</body>
</html>
    '''

# Signaling Server Socket.IO Events
@socketio.on('connect')
def handle_connect():
    user_id = str(uuid.uuid4())[:8]
    users[request.sid] = {'user_id': user_id, 'room': None}
    print(f'User connected: {user_id} ({request.sid})')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        user = users[request.sid]
        if user['room']:
            leave_room(user['room'])
            if user['room'] in rooms:
                rooms[user['room']].discard(request.sid)
                # Notify others in room
                emit('user_left', {
                    'user_id': user['user_id'],
                    'users': len(rooms[user['room']])
                }, room=user['room'])
                
                # Clean up empty rooms
                if len(rooms[user['room']]) == 0:
                    del rooms[user['room']]
        
        del users[request.sid]
        print(f'User disconnected: {user["user_id"]} ({request.sid})')

@socketio.on('join_room')
def handle_join_room(data):
    room_name = data['room']
    user = users[request.sid]
    
    # Leave current room if any
    if user['room']:
        leave_room(user['room'])
        if user['room'] in rooms:
            rooms[user['room']].discard(request.sid)
    
    # Join new room
    join_room(room_name)
    user['room'] = room_name
    
    # Initialize room if needed
    if room_name not in rooms:
        rooms[room_name] = set()
    
    rooms[room_name].add(request.sid)
    
    # Notify user
    emit('room_joined', {
        'room': room_name,
        'users': len(rooms[room_name])
    })
    
    # Notify others in room
    emit('user_joined', {
        'user_id': user['user_id'],
        'users': len(rooms[room_name])
    }, room=room_name, include_self=False)
    
    print(f'User {user["user_id"]} joined room {room_name}')

@socketio.on('leave_room')
def handle_leave_room(data):
    room_name = data['room']
    user = users[request.sid]
    
    if user['room'] == room_name:
        leave_room(room_name)
        user['room'] = None
        
        if room_name in rooms:
            rooms[room_name].discard(request.sid)
            
            # Notify others
            emit('user_left', {
                'user_id': user['user_id'],
                'users': len(rooms[room_name])
            }, room=room_name)
            
            # Clean up empty rooms
            if len(rooms[room_name]) == 0:
                del rooms[room_name]
        
        # Notify user
        emit('room_left')
        print(f'User {user["user_id"]} left room {room_name}')

@socketio.on('offer')
def handle_offer(data):
    room_name = data['room']
    # Forward offer to others in room
    emit('offer', data, room=room_name, include_self=False)
    print(f'Forwarded offer in room {room_name}')

@socketio.on('answer')
def handle_answer(data):
    room_name = data['room']
    # Forward answer to others in room
    emit('answer', data, room=room_name, include_self=False)
    print(f'Forwarded answer in room {room_name}')

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    room_name = data['room']
    # Forward ICE candidate to others in room
    emit('ice_candidate', data, room=room_name, include_self=False)

@app.route('/rooms')
def list_rooms():
    return {
        'rooms': {room: len(users) for room, users in rooms.items()},
        'total_users': len(users)
    }

if __name__ == '__main__':
    print("🔗 Starting P2P WebRTC Signaling Server...")
    print("📡 This provides the signaling for peer-to-peer connections")
    print("🌐 Access at: http://localhost:4000")
    print("🎥 Features: Room-based video chat, real-time signaling")
    print("🔧 Press Ctrl+C to stop")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=4000)
