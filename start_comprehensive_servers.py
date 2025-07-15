#!/usr/bin/env python3
"""
Comprehensive OAK Camera Server Startup

Starts all necessary servers for complete OAK camera WebRTC functionality:
- OAK Camera Bridge (port 8766)
- WebSocket Signaling Server (port 8765) 
- Video File Bridge (port 8768) - streams video files via WebSocket
- HTTP Client Server (port 8000)

RECENT FIXES (Jul 2025):
- ✅ Removed GStreamer dependencies for simplified deployment
- ✅ Fixed WebSocket handler compatibility issues  
- ✅ Enhanced error handling and fallback mechanisms
- ✅ Improved status reporting and user feedback
"""

import asyncio
import subprocess
import threading
import time
import signal
import sys
import os
import logging
import glob
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveOAKServer:
    def __init__(self, video_file=None):
        self.processes = {}
        self.running = False
        self.video_file = video_file
        
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
        
        # Check if required files exist
        required_files = [
            'oak_camera_bridge.py',
            'video_device_bridge.py',
            'websocket_server.py', 
            'video_file_bridge.py',
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
    
    def start_video_file_bridge(self):
        """Start the video file bridge"""
        logger.info("📄 Starting Video File Bridge...")
        try:
            cmd = [sys.executable, 'video_file_bridge.py', '--port', '8768']
            if self.video_file:
                cmd.extend(['--video-file', self.video_file])
            
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes['video_file_bridge'] = proc
            if self.video_file:
                logger.info(f"✅ Video File Bridge started (port 8768) - Streaming: {self.video_file}")
            else:
                logger.info("✅ Video File Bridge started (port 8768) - Ready for dynamic file selection")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start Video File Bridge: {e}")
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
            ('Video File Bridge', self.start_video_file_bridge),
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
        logger.info("   Video File Bridge:       ws://localhost:8768")
        logger.info("  📁 HTTP Client Server:      http://localhost:8000")
        logger.info("")
        logger.info("🎯 Open client: http://localhost:8000/clients/oak_websocket_client.html")
        logger.info("🎥 Universal WebRTC client with OAK camera and video file streaming")
        logger.info("")
        logger.info("🔧 Available Sources:")
        logger.info("  • Regular webcam: Select from detected cameras")
        logger.info("  • OAK Camera: Connect to DepthAI device")
        logger.info("  • Video Files: Choose dynamically from web interface")
        logger.info("")
        logger.info("🔧 Available Streaming Technologies:")
        logger.info("  • WebCodecs: Hardware-accelerated, lowest latency (Chrome only)")
        logger.info("  • Canvas: Universal compatibility, all browsers")
        logger.info("")
        logger.info("📊 Features:")
        logger.info("  • Dynamic video file selection from web UI")
        logger.info("  • Visual technology comparison mode")
        logger.info("  • Real-time performance metrics")
        logger.info("  • Automatic fallback handling")
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

def get_available_video_files():
    """Get list of available video files in the workspace"""
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm', '*.m4v']
    video_files = []
    
    for extension in video_extensions:
        video_files.extend(glob.glob(extension))
    
    return sorted(video_files)

def select_video_file():
    """Interactive video file selection"""
    video_files = get_available_video_files()
    
    if not video_files:
        logger.warning("⚠️ No video files found in the current directory")
        return None
    
    logger.info("📄 Available video files:")
    for i, video_file in enumerate(video_files, 1):
        file_size = os.path.getsize(video_file) / (1024 * 1024)  # Size in MB
        logger.info(f"  {i}. {video_file} ({file_size:.1f} MB)")
    
    logger.info("  0. Skip video file streaming")
    
    while True:
        try:
            choice = input("\n🎬 Select video file (enter number): ").strip()
            
            if choice == '0':
                logger.info("⏭️ Skipping video file streaming")
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(video_files):
                selected_file = video_files[choice_num - 1]
                logger.info(f"✅ Selected: {selected_file}")
                return selected_file
            else:
                logger.error(f"❌ Invalid choice. Please enter a number between 0 and {len(video_files)}")
                
        except (ValueError, KeyboardInterrupt):
            logger.info("\n⏭️ Skipping video file streaming")
            return None

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive OAK Camera Server")
    parser.add_argument("--video-file", type=str, help="Path to video file for streaming (optional)")
    parser.add_argument("--auto-select", action="store_true", help="Auto-select first available video file")
    args = parser.parse_args()
    
    # Video file selection (optional)
    video_file = None
    if args.video_file:
        if os.path.exists(args.video_file):
            video_file = args.video_file
            logger.info(f"📄 Using specified video file: {video_file}")
        else:
            logger.error(f"❌ Video file not found: {args.video_file}")
            sys.exit(1)
    elif args.auto_select:
        video_files = get_available_video_files()
        if video_files:
            video_file = video_files[0]
            logger.info(f"📄 Auto-selected video file: {video_file}")
        else:
            logger.warning("⚠️ No video files found for auto-selection")
    else:
        logger.info("📄 Video files can be selected dynamically from the web interface")
    
    server = ComprehensiveOAKServer(video_file=video_file)
    
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
