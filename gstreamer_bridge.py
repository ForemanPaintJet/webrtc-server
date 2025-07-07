#!/usr/bin/env python3
"""
GStreamer Bridge for OAK Camera

Provides real GStreamer pipeline integration for OAK camera streaming.
Uses actual gst-launch pipelines for hardware-accelerated processing.
"""

import asyncio
import websockets
import subprocess
import json
import logging
import threading
import time
import signal
import os
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GStreamerBridge:
    def __init__(self, port=8767):
        self.port = port
        self.clients = set()
        self.gst_process = None
        self.streaming = False
        self.frame_buffer = None
        
    def check_gstreamer_availability(self):
        """Check if GStreamer is available on the system"""
        try:
            result = subprocess.run(['gst-launch-1.0', '--version'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("✅ GStreamer detected: " + result.stdout.split('\n')[0])
                return True
            else:
                logger.warning("⚠️ GStreamer not available")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError) as e:
            logger.warning(f"⚠️ GStreamer not installed: {e}")
            logger.info("💡 To install GStreamer on macOS:")
            logger.info("   brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad")
            logger.info("💡 To install GStreamer on Ubuntu:")
            logger.info("   sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base")
            return False
    
    def get_available_pipelines(self):
        """Get list of available GStreamer pipelines for OAK camera"""
        pipelines = {
            'basic': {
                'name': 'Basic OAK Pipeline',
                'description': 'Simple OAK to WebRTC pipeline with basic encoding',
                'pipeline': [
                    'gst-launch-1.0',
                    'v4l2src', 'device=/dev/video0',
                    '!', 'video/x-raw,width=1280,height=720,framerate=30/1',
                    '!', 'videoconvert',
                    '!', 'x264enc', 'tune=zerolatency', 'bitrate=2000',
                    '!', 'rtph264pay',
                    '!', 'udpsink', 'host=127.0.0.1', 'port=5000'
                ]
            },
            'optimized': {
                'name': 'Hardware Accelerated Pipeline',
                'description': 'Hardware-accelerated encoding for minimal latency',
                'pipeline': [
                    'gst-launch-1.0',
                    'v4l2src', 'device=/dev/video0',
                    '!', 'video/x-raw,width=1280,height=720,framerate=30/1',
                    '!', 'videoconvert',
                    '!', 'queue', 'max-size-buffers=2',
                    '!', 'nvh264enc', 'preset=low-latency-hq', 'bitrate=3000',
                    '!', 'h264parse',
                    '!', 'rtph264pay',
                    '!', 'udpsink', 'host=127.0.0.1', 'port=5000'
                ]
            },
            'websocket': {
                'name': 'WebSocket Stream Pipeline',
                'description': 'Direct WebSocket streaming with JPEG compression',
                'pipeline': [
                    'gst-launch-1.0',
                    'v4l2src', 'device=/dev/video0',
                    '!', 'video/x-raw,width=1280,height=720,framerate=30/1',
                    '!', 'videoconvert',
                    '!', 'jpegenc', 'quality=85',
                    '!', 'multifilesink', 'location=/tmp/gst_frame_%05d.jpg',
                    'max-files=1'
                ]
            }
        }
        return pipelines
    
    def start_gstreamer_pipeline(self, pipeline_name='basic'):
        """Start a GStreamer pipeline"""
        if not self.check_gstreamer_availability():
            logger.warning("⚠️ GStreamer not available - cannot start real pipeline")
            logger.info("💡 The client will automatically fall back to optimized canvas processing")
            return False
        
        pipelines = self.get_available_pipelines()
        if pipeline_name not in pipelines:
            logger.error(f"Pipeline '{pipeline_name}' not found")
            return False
        
        pipeline_config = pipelines[pipeline_name]
        logger.info(f"🚀 Starting GStreamer pipeline: {pipeline_config['name']}")
        logger.info(f"Description: {pipeline_config['description']}")
        
        try:
            # Start the GStreamer process
            self.gst_process = subprocess.Popen(
                pipeline_config['pipeline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new process group for clean termination
            )
            
            self.streaming = True
            logger.info("✅ GStreamer pipeline started successfully")
            
            # Monitor the process in a separate thread
            monitor_thread = threading.Thread(target=self._monitor_gstreamer_process)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start GStreamer pipeline: {e}")
            return False
    
    def _monitor_gstreamer_process(self):
        """Monitor GStreamer process for errors and output"""
        if not self.gst_process:
            return
            
        while self.streaming and self.gst_process.poll() is None:
            try:
                # Read stderr for GStreamer messages (non-blocking)
                if self.gst_process.stderr:
                    line = self.gst_process.stderr.readline()
                    if line:
                        message = line.decode().strip()
                        if message:
                            logger.info(f"GStreamer: {message}")
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error monitoring GStreamer: {e}")
                break
        
        if self.gst_process and self.gst_process.poll() is not None:
            returncode = self.gst_process.poll()
            if returncode != 0:
                logger.error(f"❌ GStreamer process exited with code {returncode}")
            else:
                logger.info("✅ GStreamer process exited cleanly")
    
    def stop_gstreamer_pipeline(self):
        """Stop the GStreamer pipeline"""
        if self.gst_process:
            logger.info("🛑 Stopping GStreamer pipeline...")
            self.streaming = False
            
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(self.gst_process.pid), signal.SIGTERM)
                
                # Wait for clean shutdown
                try:
                    self.gst_process.wait(timeout=5)
                    logger.info("✅ GStreamer pipeline stopped cleanly")
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't stop cleanly
                    logger.warning("⚠️ Force killing GStreamer pipeline")
                    os.killpg(os.getpgid(self.gst_process.pid), signal.SIGKILL)
                    self.gst_process.wait()
                    
            except Exception as e:
                logger.error(f"Error stopping GStreamer: {e}")
            
            self.gst_process = None
    
    async def handle_client(self, websocket):
        """Handle WebSocket client connections"""
        logger.info(f"🔗 GStreamer bridge client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            await websocket.send(json.dumps({
                'type': 'gstreamer_status',
                'available': self.check_gstreamer_availability(),
                'pipelines': list(self.get_available_pipelines().keys()),
                'streaming': self.streaming
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_command(websocket, data)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("🔌 GStreamer bridge client disconnected")
        except Exception as e:
            logger.error(f"GStreamer bridge client error: {e}")
        finally:
            self.clients.discard(websocket)
    
    async def handle_command(self, websocket, data):
        """Handle commands from WebSocket clients"""
        command = data.get('command') or data.get('type')
        
        if command == 'start_pipeline':
            pipeline_name = data.get('pipeline', 'basic')
            success = self.start_gstreamer_pipeline(pipeline_name)
            await websocket.send(json.dumps({
                'type': 'pipeline_response',
                'command': 'start',
                'success': success,
                'pipeline': pipeline_name
            }))
            
        elif command == 'stop_pipeline':
            self.stop_gstreamer_pipeline()
            await websocket.send(json.dumps({
                'type': 'pipeline_response',
                'command': 'stop',
                'success': True
            }))
            
        elif command == 'get_status':
            await websocket.send(json.dumps({
                'type': 'status',
                'streaming': self.streaming,
                'gstreamer_available': self.check_gstreamer_availability(),
                'process_running': self.gst_process is not None and self.gst_process.poll() is None
            }))
            
        elif command == 'list_pipelines':
            pipelines = self.get_available_pipelines()
            await websocket.send(json.dumps({
                'type': 'pipelines',
                'pipelines': pipelines
            }))
    
    async def start_server(self):
        """Start the GStreamer bridge WebSocket server"""
        logger.info(f"🚀 Starting GStreamer bridge server on port {self.port}")
        
        # Check GStreamer availability at startup
        if self.check_gstreamer_availability():
            logger.info("✅ GStreamer bridge ready")
        else:
            logger.warning("⚠️ GStreamer not available - bridge will run in limited mode")
        
        async with websockets.serve(self.handle_client, "localhost", self.port):
            logger.info(f"🌐 GStreamer bridge listening on ws://localhost:{self.port}")
            await asyncio.Future()  # Run forever

def main():
    """Main entry point"""
    bridge = GStreamerBridge()
    
    try:
        asyncio.run(bridge.start_server())
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down GStreamer bridge...")
        bridge.stop_gstreamer_pipeline()

if __name__ == "__main__":
    main()
