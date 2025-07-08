#!/usr/bin/env python3
"""
OAK Camera WebSocket Bridge

Streams OAK-D camera frames to WebSocket clients for WebRTC integration.
"""

import asyncio
import websockets
import depthai as dai
import cv2
import json
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OAKCameraBridge:
    def __init__(self, port=8766):
        self.port = port
        self.clients = set()
        self.pipeline = None
        self.device = None
        self.streaming = False
        self.frame_queue = None
        
    def setup_oak_pipeline(self):
        """Setup OAK camera pipeline"""
        try:
            logger.info("🔶 Setting up OAK camera pipeline...")
            
            # Create pipeline
            self.pipeline = dai.Pipeline()
            
            # Define source and output
            cam_rgb = self.pipeline.create(dai.node.ColorCamera)
            xout = self.pipeline.create(dai.node.XLinkOut)
            
            xout.setStreamName("rgb")
            
            # Properties - optimized for WebRTC
            cam_rgb.setPreviewSize(1280, 720)  # 720p for better performance
            cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
            cam_rgb.setInterleaved(False)
            cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
            cam_rgb.setFps(30)
            
            # Linking
            cam_rgb.preview.link(xout.input)
            
            logger.info("✅ OAK pipeline configured: 1280x720 @ 30fps")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up OAK pipeline: {e}")
            return False
    
    def start_oak_device(self):
        """Start OAK device connection"""
        try:
            if not self.pipeline:
                if not self.setup_oak_pipeline():
                    return False
            
            logger.info("🔗 Connecting to OAK device...")
            self.device = dai.Device(self.pipeline)
            self.frame_queue = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            
            logger.info("✅ OAK device connected successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error connecting to OAK device: {e}")
            return False
    
    def stop_oak_device(self):
        """Stop OAK device"""
        try:
            self.streaming = False
            if self.device:
                self.device.close()
                self.device = None
                self.frame_queue = None
                logger.info("🔶 OAK device disconnected")
        except Exception as e:
            logger.error(f"❌ Error disconnecting OAK device: {e}")
    
    async def stream_frames(self):
        """Stream frames from OAK camera to connected clients"""
        if not self.device or not self.frame_queue:
            logger.error("❌ OAK device not connected")
            return
        
        try:
            logger.info("🎬 Starting OAK frame streaming...")
            
            frame_count = 0
            last_report = time.time()
            
            while self.streaming and self.clients:
                try:
                    # Get frame from OAK camera
                    in_rgb = self.frame_queue.get()
                    
                    if in_rgb is None:
                        await asyncio.sleep(0.001)
                        continue
                    
                    # Convert to OpenCV format
                    frame = in_rgb.getCvFrame()
                    frame_count += 1
                    
                    # Encode frame as JPEG for web streaming
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]  # Good quality, reasonable size
                    _, buffer = cv2.imencode('.jpg', frame, encode_param)
                    frame_bytes = buffer.tobytes()
                    
                    # Send to all connected clients
                    if self.clients:
                        disconnected_clients = set()
                        for client in self.clients.copy():
                            try:
                                await client.send(frame_bytes)
                            except websockets.exceptions.ConnectionClosed:
                                disconnected_clients.add(client)
                            except Exception as e:
                                logger.warning(f"⚠️ Error sending frame to client: {e}")
                                disconnected_clients.add(client)
                        
                        # Remove disconnected clients
                        self.clients -= disconnected_clients
                    
                    # Report status every 5 seconds
                    current_time = time.time()
                    if current_time - last_report >= 5.0:
                        logger.info(f"📊 Streaming: {frame_count} frames sent to {len(self.clients)} clients")
                        last_report = current_time
                    
                    # Control frame rate
                    await asyncio.sleep(0.033)  # ~30 FPS
                    
                except Exception as e:
                    logger.error(f"❌ Error in frame streaming: {e}")
                    await asyncio.sleep(0.1)
            
            logger.info("🛑 Frame streaming stopped")
            
        except Exception as e:
            logger.error(f"❌ Critical error in frame streaming: {e}")
    
    async def handle_client(self, websocket, path=None):
        """Handle WebSocket client connections"""
        client_addr = websocket.remote_address
        logger.info(f"🔗 Client connected from {client_addr}")
        
        # Add client to set
        self.clients.add(websocket)
        
        # Check if camera is available
        if not getattr(self, 'oak_available', True):
            try:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "No OAK camera available in container. Check USB device access.",
                    "details": "Run container with --device=/dev/bus/usb or --privileged"
                }))
            except:
                pass
            # Keep connection open but don't try to start camera
            try:
                await websocket.wait_closed()
            except:
                pass
            finally:
                self.clients.discard(websocket)
            return
        
        # Start streaming if this is the first client
        if len(self.clients) == 1 and not self.streaming:
            logger.info("▶️ Starting OAK camera streaming for first client")
            
            # Start OAK device
            if not self.start_oak_device():
                try:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Failed to start OAK camera"
                    }))
                except:
                    pass
                self.clients.remove(websocket)
                return
            
            # Start streaming
            self.streaming = True
            asyncio.create_task(self.stream_frames())
            
            # Send success message
            try:
                await websocket.send(json.dumps({
                    "type": "connected",
                    "message": "OAK camera streaming started",
                    "resolution": "1280x720",
                    "fps": 30
                }))
            except:
                pass
        else:
            # Send connection confirmation
            try:
                await websocket.send(json.dumps({
                    "type": "connected", 
                    "message": "Connected to existing OAK stream",
                    "resolution": "1280x720",
                    "fps": 30
                }))
            except:
                pass
        
        try:
            # Keep connection alive and handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'ping':
                        await websocket.send(json.dumps({"type": "pong"}))
                except json.JSONDecodeError:
                    pass  # Ignore invalid JSON
                except:
                    break
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.warning(f"⚠️ Client connection error: {e}")
        finally:
            # Remove client
            self.clients.discard(websocket)
            logger.info(f"🔌 Client {client_addr} disconnected")
            
            # Stop streaming if no clients left
            if not self.clients and self.streaming:
                logger.info("⏹️ No clients connected, stopping OAK streaming")
                self.stop_oak_device()
    
    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🚀 Starting OAK Camera WebSocket Bridge on port {self.port}")
        logger.info("📡 Clients can connect to: ws://0.0.0.0:8766")
        
        # Start WebSocket server
        async with websockets.serve(
            self.handle_client,
            "0.0.0.0",
            self.port,
            max_size=10**7,  # 10MB max message size for frames
            ping_timeout=20,
            ping_interval=10
        ):
            logger.info("✅ OAK Camera Bridge running... (Press Ctrl+C to stop)")
            await asyncio.Future()  # run forever

def main():
    """Main function"""
    print("🔶 OAK Camera WebSocket Bridge")
    print("=" * 40)
    
    # Check if OAK camera is available
    oak_available = False
    try:
        devices = dai.Device.getAllAvailableDevices()
        if len(devices) == 0:
            # Try direct connection
            try:
                with dai.Device() as device:
                    print("✅ OAK camera detected (direct connection)")
                    oak_available = True
            except Exception as e:
                print(f"⚠️  No OAK cameras found: {e}")
                print("🔄 Starting bridge in 'no camera' mode - will keep running and retry connections")
                oak_available = False
        else:
            print(f"✅ Found {len(devices)} OAK camera(s)")
            for i, device in enumerate(devices):
                print(f"  📷 Device {i}: {device.name} ({device.mxid})")
            oak_available = True
        
    except Exception as e:
        print(f"⚠️  Error detecting OAK cameras: {e}")
        print("🔄 Starting bridge in 'no camera' mode - will keep running for Docker compatibility")
        oak_available = False
    
    # Create and start bridge (even without camera - important for Docker)
    bridge = OAKCameraBridge(port=8766)
    bridge.oak_available = getattr(bridge, 'oak_available', oak_available)
    
    print(f"🌐 Starting WebSocket server on port 8766...")
    if not oak_available:
        print("📝 Note: Bridge will respond with 'no camera' messages until OAK camera is connected")
    
    try:
        asyncio.run(bridge.start_server())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down OAK Camera Bridge...")
        bridge.stop_oak_device()

if __name__ == "__main__":
    main()
