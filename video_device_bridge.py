#!/usr/bin/env python3
"""
Video Device WebSocket Bridge (/dev/video0)

Streams frames from a standard video device (e.g., webcam at /dev/video0) to WebSocket clients for WebRTC integration.
"""

import asyncio
import websockets
import cv2
import json
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoDeviceBridge:
    def __init__(self, port=8769, device_path="/dev/video0"):
        self.port = port
        self.device_path = device_path
        self.clients = set()
        self.streaming = False
        self.cap = None

    def start_video_device(self):
        """Start /dev/video0 device connection"""
        try:
            logger.info(f"🔗 Connecting to {self.device_path} ...")
            self.cap = cv2.VideoCapture(self.device_path)
            if not self.cap.isOpened():
                logger.error(f"❌ Could not open {self.device_path}")
                return False
            # Set resolution (optional)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            logger.info(f"✅ {self.device_path} opened successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error opening {self.device_path}: {e}")
            return False

    def stop_video_device(self):
        """Stop /dev/video0 device"""
        try:
            self.streaming = False
            if self.cap:
                self.cap.release()
                self.cap = None
                logger.info(f"🔶 {self.device_path} released")
        except Exception as e:
            logger.error(f"❌ Error releasing {self.device_path}: {e}")

    async def stream_frames(self):
        """Stream frames from /dev/video0 to connected clients"""
        if not self.cap or not self.cap.isOpened():
            logger.error(f"❌ {self.device_path} not opened")
            return

        try:
            logger.info(f"🎬 Starting {self.device_path} frame streaming...")
            frame_count = 0
            last_report = time.time()

            while self.streaming and self.clients:
                try:
                    ret, frame = self.cap.read()
                    if not ret:
                        await asyncio.sleep(0.001)
                        continue

                    frame_count += 1
                    # Encode frame as JPEG for web streaming
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
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

        # Start streaming if this is the first client
        if len(self.clients) == 1 and not self.streaming:
            logger.info(f"▶️ Starting {self.device_path} streaming for first client")

            # Start video device
            if not self.start_video_device():
                try:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Failed to open {self.device_path}"
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
                    "message": f"{self.device_path} streaming started",
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
                    "message": f"Connected to existing {self.device_path} stream",
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
                logger.info(f"⏹️ No clients connected, stopping {self.device_path} streaming")
                self.stop_video_device()

    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🚀 Starting Video Device WebSocket Bridge on port {self.port}")
        logger.info(f"📡 Clients can connect to: ws://0.0.0.0:{self.port}")

        # Start WebSocket server
        async with websockets.serve(
            self.handle_client,
            "0.0.0.0",
            self.port,
            max_size=10**7,  # 10MB max message size for frames
            ping_timeout=20,
            ping_interval=10
        ):
            logger.info("✅ Video Device Bridge running... (Press Ctrl+C to stop)")
            await asyncio.Future()  # run forever

def main():
    """Main function"""
    print("🔶 Video Device WebSocket Bridge (/dev/video0)")
    print("=" * 40)

    # Create and start bridge
    bridge = VideoDeviceBridge(port=8769, device_path="/dev/video0")

    print(f"🌐 Starting WebSocket server on port 8769...")

    try:
        asyncio.run(bridge.start_server())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Video Device Bridge...")
        bridge.stop_video_device()

if __name__ == "__main__":
    main()
