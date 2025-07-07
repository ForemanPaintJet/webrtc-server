#!/usr/bin/env python3
"""
OAK Camera Bridge with Raw Frame Streaming
Alternative version that sends raw frame data instead of JPEG
"""

import asyncio
import websockets
import depthai as dai
import cv2
import json
import numpy as np
import logging

class OAKRawFrameBridge:
    def __init__(self, port=8767):  # Different port to avoid conflicts
        self.port = port
        self.clients = set()
        self.pipeline = None
        self.device = None
        self.streaming = False
        self.frame_queue = None
        
    async def stream_raw_frames(self):
        """Stream raw frame data to connected clients"""
        while self.streaming and self.clients:
            try:
                # Get frame from OAK camera
                in_rgb = self.frame_queue.get()
                if in_rgb is None:
                    await asyncio.sleep(0.001)
                    continue
                
                # Get raw frame data
                frame = in_rgb.getCvFrame()
                
                # Convert to format suitable for web (RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Send raw frame data as binary
                # Format: width(4) + height(4) + frame_data
                height, width = frame_rgb.shape[:2]
                frame_data = frame_rgb.tobytes()
                
                # Create header with dimensions
                header = width.to_bytes(4, byteorder='little') + height.to_bytes(4, byteorder='little')
                message = header + frame_data
                
                # Send to all connected clients
                if self.clients:
                    disconnected_clients = set()
                    for client in self.clients.copy():
                        try:
                            await client.send(message)
                        except websockets.exceptions.ConnectionClosed:
                            disconnected_clients.add(client)
                        except Exception as e:
                            disconnected_clients.add(client)
                    
                    # Remove disconnected clients
                    self.clients -= disconnected_clients
                
                # Control frame rate
                await asyncio.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in frame streaming: {e}")
                await asyncio.sleep(0.1)

    async def handle_client(self, websocket, path=None):
        """Handle WebSocket client connections"""
        print(f"Raw frame client connected from {websocket.remote_address}")
        self.clients.add(websocket)
        
        # Send connection info
        await websocket.send(json.dumps({
            "type": "connected",
            "message": "Raw frame streaming",
            "format": "RGB888",
            "width": 1280,
            "height": 720
        }))
        
        try:
            # Start streaming if first client
            if len(self.clients) == 1 and not self.streaming:
                self.start_oak_device()
                self.streaming = True
                asyncio.create_task(self.stream_raw_frames())
            
            # Keep connection alive
            async for message in websocket:
                pass  # Handle client messages if needed
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            if not self.clients:
                self.streaming = False
