#!/usr/bin/env python3
"""
GStreamer Bridge (Fallback Mode)

Provides GStreamer integration when available, or operates in fallback mode
when GStreamer is not installed on the system.
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

class GStreamerBridgeFallback:
    def __init__(self, port=8767):
        self.port = port
        self.clients = set()
        self.gst_process = None
        self.streaming = False
        self.gstreamer_available = False
        
    def check_gstreamer_availability(self):
        """Check if GStreamer is available on the system"""
        try:
            result = subprocess.run(['gst-launch-1.0', '--version'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("✅ GStreamer detected: " + result.stdout.split('\n')[0])
                self.gstreamer_available = True
                return True
            else:
                logger.warning("⚠️ GStreamer not available")
                self.gstreamer_available = False
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError) as e:
            logger.warning(f"⚠️ GStreamer check failed: {e}")
            logger.info("💡 To install GStreamer:")
            logger.info("   macOS: brew install gstreamer gst-plugins-base gst-plugins-good")
            logger.info("   Ubuntu: sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base")
            self.gstreamer_available = False
            return False
    
    def get_available_pipelines(self):
        """Get list of available GStreamer pipelines"""
        if not self.gstreamer_available:
            return {
                'fallback': {
                    'name': 'Fallback Canvas Processing',
                    'description': 'Optimized canvas processing that mimics GStreamer behavior',
                    'available': True
                }
            }
        
        pipelines = {
            'basic': {
                'name': 'Basic OAK Pipeline',
                'description': 'Simple OAK to WebRTC pipeline with basic encoding',
                'available': True
            },
            'optimized': {
                'name': 'Hardware Accelerated Pipeline',
                'description': 'Hardware-accelerated encoding for minimal latency',
                'available': True
            },
            'websocket': {
                'name': 'WebSocket Stream Pipeline',
                'description': 'Direct WebSocket streaming with JPEG compression',
                'available': True
            }
        }
        return pipelines
    
    def start_pipeline(self, pipeline_name='basic'):
        """Start a pipeline (real GStreamer or fallback)"""
        pipelines = self.get_available_pipelines()
        if pipeline_name not in pipelines:
            logger.error(f"Pipeline '{pipeline_name}' not found")
            return False
        
        pipeline_config = pipelines[pipeline_name]
        logger.info(f"🚀 Starting pipeline: {pipeline_config['name']}")
        logger.info(f"Description: {pipeline_config['description']}")
        
        if self.gstreamer_available and pipeline_name != 'fallback':
            return self._start_real_gstreamer_pipeline(pipeline_name)
        else:
            return self._start_fallback_pipeline(pipeline_name)
    
    def _start_real_gstreamer_pipeline(self, pipeline_name):
        """Start actual GStreamer pipeline"""
        logger.info("🚀 Starting real GStreamer pipeline...")
        
        # Example pipelines - would need real implementation based on your setup
        pipeline_commands = {
            'basic': [
                'gst-launch-1.0',
                'videotestsrc', 'pattern=ball',
                '!', 'video/x-raw,width=1280,height=720,framerate=30/1',
                '!', 'videoconvert',
                '!', 'x264enc', 'tune=zerolatency', 'bitrate=2000',
                '!', 'fakesink'
            ],
            'optimized': [
                'gst-launch-1.0',
                'videotestsrc', 'pattern=ball',
                '!', 'video/x-raw,width=1280,height=720,framerate=30/1',
                '!', 'videoconvert',
                '!', 'queue', 'max-size-buffers=2',
                '!', 'x264enc', 'preset=ultrafast', 'tune=zerolatency',
                '!', 'fakesink'
            ]
        }
        
        if pipeline_name not in pipeline_commands:
            logger.error(f"No command defined for pipeline: {pipeline_name}")
            return False
        
        try:
            self.gst_process = subprocess.Popen(
                pipeline_commands[pipeline_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.streaming = True
            logger.info("✅ Real GStreamer pipeline started successfully")
            
            # Monitor in background
            monitor_thread = threading.Thread(target=self._monitor_gstreamer_process)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start real GStreamer pipeline: {e}")
            return False
    
    def _start_fallback_pipeline(self, pipeline_name):
        """Start fallback pipeline simulation"""
        logger.info("🔄 Starting fallback pipeline (simulated GStreamer behavior)...")
        self.streaming = True
        logger.info("✅ Fallback pipeline started - client will use optimized canvas processing")
        return True
    
    def _monitor_gstreamer_process(self):
        """Monitor real GStreamer process"""
        if not self.gst_process:
            return
            
        while self.streaming and self.gst_process.poll() is None:
            try:
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
    
    def stop_pipeline(self):
        """Stop the current pipeline"""
        if self.gst_process:
            logger.info("🛑 Stopping GStreamer pipeline...")
            self.streaming = False
            
            try:
                os.killpg(os.getpgid(self.gst_process.pid), signal.SIGTERM)
                try:
                    self.gst_process.wait(timeout=5)
                    logger.info("✅ GStreamer pipeline stopped cleanly")
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ Force killing GStreamer pipeline")
                    os.killpg(os.getpgid(self.gst_process.pid), signal.SIGKILL)
                    self.gst_process.wait()
            except Exception as e:
                logger.error(f"Error stopping GStreamer: {e}")
            
            self.gst_process = None
        else:
            logger.info("🛑 Stopping fallback pipeline...")
            self.streaming = False
    
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connections"""
        logger.info(f"🔗 GStreamer bridge client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            # Send initial status
            await websocket.send(json.dumps({
                'type': 'gstreamer_status',
                'available': self.gstreamer_available,
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
        command = data.get('command')
        
        if command == 'start_pipeline':
            pipeline_name = data.get('pipeline', 'basic')
            success = self.start_pipeline(pipeline_name)
            await websocket.send(json.dumps({
                'type': 'pipeline_response',
                'command': 'start',
                'success': success,
                'pipeline': pipeline_name
            }))
            
        elif command == 'stop_pipeline':
            self.stop_pipeline()
            await websocket.send(json.dumps({
                'type': 'pipeline_response',
                'command': 'stop',
                'success': True
            }))
            
        elif command == 'get_status':
            await websocket.send(json.dumps({
                'type': 'status',
                'streaming': self.streaming,
                'gstreamer_available': self.gstreamer_available,
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
        self.check_gstreamer_availability()
        
        if self.gstreamer_available:
            logger.info("✅ GStreamer bridge ready with real GStreamer support")
        else:
            logger.info("⚠️ GStreamer bridge running in fallback mode")
        
        async with websockets.serve(self.handle_client, "localhost", self.port):
            logger.info(f"🌐 GStreamer bridge listening on ws://localhost:{self.port}")
            await asyncio.Future()  # Run forever

def main():
    """Main entry point"""
    bridge = GStreamerBridgeFallback()
    
    try:
        asyncio.run(bridge.start_server())
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down GStreamer bridge...")
        bridge.stop_pipeline()

if __name__ == "__main__":
    main()
