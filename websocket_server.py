#!/usr/bin/env python3
"""
Pure WebSocket Signaling Server for WebRTC P2P

Standalone WebSocket server for WebRTC signaling without Flask.
Run this separately from the HTTP server.
"""

import json
import uuid
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebRTCSignalingServer:
    def __init__(self):
        self.rooms = {}
        self.connections = {}
    
    async def register_user(self, websocket):
        """Register a new WebSocket connection"""
        user_id = str(uuid.uuid4())[:8]
        self.connections[websocket] = {
            'user_id': user_id,
            'room': None,
            'websocket': websocket
        }
        logger.info(f"User connected: {user_id}")
        
        # Send welcome message
        await websocket.send(json.dumps({
            'type': 'connected',
            'user_id': user_id
        }))
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except ConnectionClosed:
            logger.info(f"Connection closed for user: {user_id}")
        except Exception as e:
            logger.error(f"Error handling connection for user {user_id}: {e}")
        finally:
            await self.unregister_user(websocket)
    
    async def unregister_user(self, websocket):
        """Remove user and clean up"""
        if websocket in self.connections:
            user = self.connections[websocket]
            user_id = user['user_id']
            room = user['room']
            
            # Leave room if in one
            if room and room in self.rooms:
                self.rooms[room].discard(websocket)
                
                # Notify others in room
                await self.broadcast_to_room(room, {
                    'type': 'user_left',
                    'user_id': user_id,
                    'users': len(self.rooms[room])
                }, exclude=websocket)
                
                # Clean up empty rooms
                if len(self.rooms[room]) == 0:
                    del self.rooms[room]
                    logger.info(f"Room {room} cleaned up (empty)")
            
            del self.connections[websocket]
            logger.info(f"User disconnected: {user_id}")
    
    async def handle_message(self, websocket, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            logger.debug(f"Received message: {message_type}")
            
            if message_type == 'join_room':
                await self.handle_join_room(websocket, data)
            elif message_type == 'leave_room':
                await self.handle_leave_room(websocket, data)
            elif message_type == 'offer':
                await self.handle_offer(websocket, data)
            elif message_type == 'answer':
                await self.handle_answer(websocket, data)
            elif message_type == 'ice_candidate':
                await self.handle_ice_candidate(websocket, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def handle_join_room(self, websocket, data):
        """Handle room join request"""
        room_name = data['room']
        user = self.connections[websocket]
        
        # Leave current room if any
        if user['room'] and user['room'] in self.rooms:
            self.rooms[user['room']].discard(websocket)
        
        # Join new room
        user['room'] = room_name
        if room_name not in self.rooms:
            self.rooms[room_name] = set()
        
        self.rooms[room_name].add(websocket)
        
        # Notify user
        await websocket.send(json.dumps({
            'type': 'room_joined',
            'room': room_name,
            'users': len(self.rooms[room_name])
        }))
        
        # Notify others in room
        await self.broadcast_to_room(room_name, {
            'type': 'user_joined',
            'user_id': user['user_id'],
            'users': len(self.rooms[room_name])
        }, exclude=websocket)
        
        logger.info(f"User {user['user_id']} joined room {room_name} ({len(self.rooms[room_name])} users)")
    
    async def handle_leave_room(self, websocket, data):
        """Handle room leave request"""
        user = self.connections[websocket]
        room_name = user['room']
        
        if room_name and room_name in self.rooms:
            self.rooms[room_name].discard(websocket)
            user['room'] = None
            
            # Notify others
            await self.broadcast_to_room(room_name, {
                'type': 'user_left',
                'user_id': user['user_id'],
                'users': len(self.rooms[room_name])
            })
            
            # Clean up empty rooms
            if len(self.rooms[room_name]) == 0:
                del self.rooms[room_name]
                logger.info(f"Room {room_name} cleaned up (empty)")
            
            # Notify user
            await websocket.send(json.dumps({
                'type': 'room_left'
            }))
            
            logger.info(f"User {user['user_id']} left room {room_name}")
    
    async def handle_offer(self, websocket, data):
        """Forward WebRTC offer to other users in room"""
        user = self.connections[websocket]
        room_name = user['room']
        
        if room_name:
            await self.broadcast_to_room(room_name, {
                'type': 'offer',
                'offer': data['offer'],
                'from_user': user['user_id']
            }, exclude=websocket)
            
            logger.info(f"Forwarded offer from {user['user_id']} in room {room_name}")
    
    async def handle_answer(self, websocket, data):
        """Forward WebRTC answer to other users in room"""
        user = self.connections[websocket]
        room_name = user['room']
        
        if room_name:
            await self.broadcast_to_room(room_name, {
                'type': 'answer',
                'answer': data['answer'],
                'from_user': user['user_id']
            }, exclude=websocket)
            
            logger.info(f"Forwarded answer from {user['user_id']} in room {room_name}")
    
    async def handle_ice_candidate(self, websocket, data):
        """Forward ICE candidate to other users in room"""
        user = self.connections[websocket]
        room_name = user['room']
        
        if room_name:
            await self.broadcast_to_room(room_name, {
                'type': 'ice_candidate',
                'candidate': data['candidate'],
                'from_user': user['user_id']
            }, exclude=websocket)
            
            logger.debug(f"Forwarded ICE candidate from {user['user_id']} in room {room_name}")
    
    async def broadcast_to_room(self, room_name, message, exclude=None):
        """Send message to all users in a room"""
        if room_name in self.rooms:
            disconnected = []
            for ws in self.rooms[room_name]:
                if ws != exclude:
                    try:
                        await ws.send(json.dumps(message))
                    except ConnectionClosed:
                        disconnected.append(ws)
                    except Exception as e:
                        logger.error(f"Error sending message to user: {e}")
                        disconnected.append(ws)
            
            # Clean up disconnected websockets
            for ws in disconnected:
                self.rooms[room_name].discard(ws)
                if ws in self.connections:
                    del self.connections[ws]

# Global signaling server instance
signaling_server = WebRTCSignalingServer()

async def websocket_handler(websocket):
    """WebSocket connection handler"""
    await signaling_server.register_user(websocket)

async def main():
    """Main WebSocket server"""
    
    print("🔗 Starting Pure WebSocket Signaling Server...")
    print("📡 WebSocket URL: ws://localhost:8765")
    print("🎥 Features: Room-based WebRTC signaling")
    print("🧪 Test with: websocat ws://localhost:8765")
    print("🔧 Press Ctrl+C to stop")
    print("")
    
    try:
        async with websockets.serve(
            websocket_handler, 
            "0.0.0.0", 
            8765,
            ping_interval=20,  # Keep connections alive
            ping_timeout=10
        ):
            logger.info("✅ WebSocket server started on ws://0.0.0.0:8765")
            await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
