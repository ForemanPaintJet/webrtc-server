#!/usr/bin/env python3
"""
Comprehensive OAK Camera Server Startup

Starts all necessary servers for complete OAK camera WebRTC functionality:
- OAK Camera Bridge (port 8766)
- WebSocket Signaling Server (port 8765) 
- GStreamer Bridge (port 8767) - with real GStreamer integration
- HTTP Client Server (port 8000)

RECENT FIXES (Jul 2025):
- ✅ Fixed GStreamer detection and installation support
- ✅ Fixed WebSocket handler compatibility issues  
- ✅ Enhanced error handling and fallback mechanisms
- ✅ Added clear installation instructions for macOS/Ubuntu
- ✅ Improved status reporting and user feedback

GStreamer Installation:
  macOS: brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad
  Ubuntu: sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base
"""

import asyncio
import subprocess
import threading
import time
import signal
import sys
import os
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveOAKServer:
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def check_requirements(self):
        """Check if all required dependencies are available"""
        logger.info("🔍 Checking system requirements...")
        
        # Check Python modules
        required_modules = {
            'depthai': 'pip install depthai',
            'cv2': 'pip install opencv-python', 
            'websockets': 'pip install websockets',
            'asyncio': 'Built-in module'
        }
        
        missing_modules = []
        for module, install_cmd in required_modules.items():
            try:
                __import__(module)
                logger.info(f"✅ {module} available")
            except ImportError:
                logger.error(f"❌ {module} not available - Install with: {install_cmd}")
                missing_modules.append(module)
        
        if missing_modules:
            logger.error("❌ Missing required modules. Install all dependencies with:")
            logger.error("   pip install -r requirements.txt")
            return False
        
        # Check GStreamer
        try:
            result = subprocess.run(['gst-launch-1.0', '--version'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                logger.info(f"✅ GStreamer available: {version}")
            else:
                logger.warning("⚠️ GStreamer not available - GStreamer bridge will run in fallback mode")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("⚠️ GStreamer not available - GStreamer bridge will run in fallback mode")
        
        # Check if required files exist
        required_files = [
            'oak_camera_bridge.py',
            'websocket_server.py', 
            'gstreamer_bridge.py',
            'clients/oak_websocket_client.html'
        ]
        
        for file_path in required_files:
            if not Path(file_path).exists():
                logger.error(f"❌ Required file not found: {file_path}")
                return False
            logger.info(f"✅ {file_path} found")
        
        return True
    
    def start_oak_camera_bridge(self):
        """Start the OAK camera bridge"""
        logger.info("🔶 Starting OAK Camera Bridge...")
        try:
            proc = subprocess.Popen([
                sys.executable, 'oak_camera_bridge.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes['oak_bridge'] = proc
            logger.info("✅ OAK Camera Bridge started (port 8766)")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start OAK Camera Bridge: {e}")
            return False
    
    def start_websocket_server(self):
        """Start the WebSocket signaling server"""
        logger.info("🌐 Starting WebSocket Signaling Server...")
        try:
            proc = subprocess.Popen([
                sys.executable, 'websocket_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes['websocket_server'] = proc
            logger.info("✅ WebSocket Signaling Server started (port 8765)")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start WebSocket Signaling Server: {e}")
            return False
    
    def start_gstreamer_bridge(self):
        """Start the GStreamer bridge"""
        logger.info("🚀 Starting GStreamer Bridge...")
        try:
            proc = subprocess.Popen([
                sys.executable, 'gstreamer_bridge.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes['gstreamer_bridge'] = proc
            logger.info("✅ GStreamer Bridge started (port 8767)")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start GStreamer Bridge: {e}")
            return False
    
    def start_http_server(self):
        """Start HTTP server for client files"""
        logger.info("📁 Starting HTTP Server for clients...")
        try:
            proc = subprocess.Popen([
                sys.executable, '-m', 'http.server', '8000'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes['http_server'] = proc
            logger.info("✅ HTTP Server started (port 8000)")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start HTTP Server: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        while self.running:
            for name, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    logger.warning(f"⚠️ Process {name} exited with code {proc.returncode}")
                    # Optionally restart the process here
                    
            time.sleep(5)
    
    def start_all_servers(self):
        """Start all servers"""
        if not self.check_requirements():
            logger.error("❌ Requirements check failed")
            return False
        
        logger.info("🚀 Starting comprehensive OAK camera server stack...")
        self.running = True
        
        # Start all servers
        servers = [
            ('OAK Camera Bridge', self.start_oak_camera_bridge),
            ('WebSocket Signaling Server', self.start_websocket_server),
            ('GStreamer Bridge', self.start_gstreamer_bridge),
            ('HTTP Server', self.start_http_server)
        ]
        
        for name, start_func in servers:
            if not start_func():
                logger.error(f"❌ Failed to start {name}")
                self.stop_all_servers()
                return False
            time.sleep(1)  # Brief delay between starts
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        logger.info("✅ All servers started successfully!")
        logger.info("")
        logger.info("📊 Server Status:")
        logger.info("  🔶 OAK Camera Bridge:       ws://localhost:8766")
        logger.info("  🌐 WebSocket Signaling:     ws://localhost:8765") 
        logger.info("  🚀 GStreamer Bridge:        ws://localhost:8767")
        logger.info("  📁 HTTP Client Server:      http://localhost:8000")
        logger.info("")
        logger.info("🎯 Open client: http://localhost:8000/clients/oak_websocket_client.html")
        logger.info("🎥 Universal WebRTC client with OAK camera and streaming tech comparison")
        logger.info("")
        logger.info("🔧 Available Streaming Technologies:")
        logger.info("  • WebCodecs: Hardware-accelerated, lowest latency (Chrome only)")
        logger.info("  • GStreamer: Real pipelines with hardware acceleration + fallback")
        logger.info("  • Canvas: Universal compatibility, all browsers")
        logger.info("")
        logger.info("📊 Features:")
        logger.info("  • Visual technology comparison mode")
        logger.info("  • Real-time performance metrics")
        logger.info("  • Automatic fallback handling")
        logger.info("  • Export comparison reports")
        logger.info("")
        logger.info("Press Ctrl+C to stop all servers")
        
        return True
    
    def stop_all_servers(self):
        """Stop all servers"""
        logger.info("🛑 Stopping all servers...")
        self.running = False
        
        for name, proc in self.processes.items():
            if proc.poll() is None:
                logger.info(f"🛑 Stopping {name}...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    logger.info(f"✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ Force killing {name}")
                    proc.kill()
                    proc.wait()
        
        self.processes.clear()
        logger.info("✅ All servers stopped")
    
    def handle_signal(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum}")
        self.stop_all_servers()
        sys.exit(0)

def main():
    """Main entry point"""
    server = ComprehensiveOAKServer()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, server.handle_signal)
    signal.signal(signal.SIGTERM, server.handle_signal)
    
    try:
        if server.start_all_servers():
            # Keep the main process running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            logger.error("❌ Failed to start servers")
            sys.exit(1)
            
    finally:
        server.stop_all_servers()

if __name__ == "__main__":
    main()
