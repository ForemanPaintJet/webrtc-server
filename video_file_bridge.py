#!/usr/bin/env python3
"""
Video File WebSocket Bridge

Streams a video file to WebSocket clients for WebRTC integration.
"""

import asyncio
import websockets
import cv2
import json
import logging
import time
import argparse
import glob
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoFileBridge:
    def __init__(self, port=8768, video_file=None):
        self.port = port
        self.clients = set()
        self.streaming = False
        self.video_file = video_file
        self.video_capture = None
        self.current_video_info = None

    def setup_video_source(self):
        """Setup video source from a file"""
        if not self.video_file:
            logger.error("❌ No video file specified.")
            return False
        
        try:
            logger.info(f"🔶 Opening video file: {self.video_file}")
            self.video_capture = cv2.VideoCapture(self.video_file)
            if not self.video_capture.isOpened():
                logger.error(f"❌ Error opening video file: {self.video_file}")
                return False
            
            # Get video properties
            self.width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"✅ Video file opened successfully: {self.width}x{self.height} @ {self.fps:.2f} FPS")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up video source: {e}")
            return False

    def stop_video_source(self):
        """Stop video source"""
        self.streaming = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
            logger.info("🔶 Video source stopped")

    def get_available_video_files(self):
        """Get list of available video files"""
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm', '*.m4v']
        video_files = []
        
        for extension in video_extensions:
            video_files.extend(glob.glob(extension))
        
        # Get file info
        file_info = []
        for file_path in sorted(video_files):
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                # Try to get video info
                temp_cap = cv2.VideoCapture(file_path)
                if temp_cap.isOpened():
                    width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = temp_cap.get(cv2.CAP_PROP_FPS)
                    duration = temp_cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps if fps > 0 else 0
                    temp_cap.release()
                    
                    file_info.append({
                        'name': file_path,
                        'size_mb': round(size_mb, 1),
                        'width': width,
                        'height': height,
                        'fps': round(fps, 2),
                        'duration': round(duration, 1)
                    })
                else:
                    file_info.append({
                        'name': file_path,
                        'size_mb': round(size_mb, 1),
                        'error': 'Cannot read video file'
                    })
            except Exception as e:
                file_info.append({
                    'name': file_path,
                    'error': str(e)
                })
        
        return file_info

    def change_video_file(self, new_video_file):
        """Change the current video file"""
        if self.streaming:
            self.stop_video_source()
        
        self.video_file = new_video_file
        logger.info(f"📄 Changed video file to: {new_video_file}")
        
        # If there are connected clients, restart streaming with new file
        if self.clients:
            return self.setup_video_source()
        return True

    async def stream_frames(self):
        """Stream frames from video file to connected clients"""
        if not self.video_capture:
            logger.error("❌ Video source not ready")
            return
        
        try:
            logger.info("🎬 Starting video frame streaming...")
            
            frame_count = 0
            last_report = time.time()
            
            while self.streaming and self.clients:
                try:
                    ret, frame = self.video_capture.read()
                    if not ret:
                        logger.info("🔄 Reached end of video, restarting from beginning.")
                        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
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
                    
                    current_time = time.time()
                    if current_time - last_report >= 5.0:
                        logger.info(f"📊 Streaming: {frame_count} frames sent to {len(self.clients)} clients")
                        last_report = current_time
                    
                    # Control frame rate
                    await asyncio.sleep(1 / self.fps)
                    
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
        
        self.clients.add(websocket)
        
        if len(self.clients) == 1 and not self.streaming:
            logger.info("▶️ Starting video streaming for first client")
            
            if not self.setup_video_source():
                try:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Failed to start video source"
                    }))
                except:
                    pass
                self.clients.remove(websocket)
                return
            
            self.streaming = True
            asyncio.create_task(self.stream_frames())
            
            try:
                await websocket.send(json.dumps({
                    "type": "connected",
                    "message": "Video file streaming started",
                    "resolution": f"{self.width}x{self.height}",
                    "fps": self.fps
                }))
            except:
                pass
        else:
            try:
                await websocket.send(json.dumps({
                    "type": "connected", 
                    "message": "Connected to existing video stream",
                    "resolution": f"{self.width}x{self.height}",
                    "fps": self.fps
                }))
            except:
                pass
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get('type')
                    
                    if message_type == 'ping':
                        await websocket.send(json.dumps({"type": "pong"}))
                    
                    elif message_type == 'list_files':
                        # Send list of available video files
                        files = self.get_available_video_files()
                        await websocket.send(json.dumps({
                            "type": "file_list",
                            "files": files
                        }))
                    
                    elif message_type == 'change_file':
                        # Change current video file
                        new_file = data.get('file')
                        if new_file:
                            success = self.change_video_file(new_file)
                            if success:
                                # Restart streaming if we have the video source
                                if self.video_capture and not self.streaming:
                                    self.streaming = True
                                    asyncio.create_task(self.stream_frames())
                                
                                # Send success response with video info
                                await websocket.send(json.dumps({
                                    "type": "file_changed",
                                    "success": True,
                                    "file": new_file,
                                    "resolution": f"{self.width}x{self.height}" if hasattr(self, 'width') else "Unknown",
                                    "fps": getattr(self, 'fps', 0)
                                }))
                            else:
                                await websocket.send(json.dumps({
                                    "type": "file_changed", 
                                    "success": False,
                                    "error": f"Failed to load video file: {new_file}"
                                }))
                        else:
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": "No file specified"
                            }))
                    
                    elif message_type == 'get_current_file':
                        # Send current file info
                        await websocket.send(json.dumps({
                            "type": "current_file",
                            "file": self.video_file,
                            "resolution": f"{self.width}x{self.height}" if hasattr(self, 'width') else "Unknown",
                            "fps": getattr(self, 'fps', 0),
                            "streaming": self.streaming
                        }))
                        
                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    logger.warning(f"⚠️ Error processing message: {e}")
                    break
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.warning(f"⚠️ Client connection error: {e}")
        finally:
            self.clients.discard(websocket)
            logger.info(f"🔌 Client {client_addr} disconnected")
            
            if not self.clients and self.streaming:
                logger.info("⏹️ No clients connected, stopping video streaming")
                self.stop_video_source()

    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🚀 Starting Video File WebSocket Bridge on port {self.port}")
        logger.info(f"📡 Clients can connect to: ws://0.0.0.0:{self.port}")
        
        # Check if we have a video file specified
        if self.video_file:
            if not os.path.exists(self.video_file):
                logger.error(f"❌ Video file not found: {self.video_file}")
                return
            logger.info(f"📄 Pre-loaded video file: {self.video_file}")
        else:
            logger.info("📄 No video file specified - waiting for dynamic selection")
        
        async with websockets.serve(
            self.handle_client,
            "0.0.0.0",
            self.port,
            max_size=10**7,
            ping_timeout=20,
            ping_interval=10
        ):
            logger.info("✅ Video File Bridge running... (Press Ctrl+C to stop)")
            try:
                await asyncio.Future()
            except KeyboardInterrupt:
                logger.info("🛑 Received shutdown signal")
                raise

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Video File WebSocket Bridge")
    parser.add_argument("--port", type=int, default=8768, help="WebSocket server port")
    parser.add_argument("--video-file", type=str, help="Path to the video file to stream (optional)")
    args = parser.parse_args()

    print("📹 Video File WebSocket Bridge")
    print("=" * 40)
    
    bridge = VideoFileBridge(port=args.port, video_file=args.video_file)
    
    try:
        asyncio.run(bridge.start_server())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Video File Bridge...")
        bridge.stop_video_source()

if __name__ == "__main__":
    main()
