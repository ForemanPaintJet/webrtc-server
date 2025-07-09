#!/usr/bin/env python3
"""
OAK Camera Server Startup

Starts OAK camera servers with WebCodecs and Canvas streaming support.
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

class OAKServerManager:
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def check_requirements(self):
        """Check basic requirements"""
        logger.info("🔍 Checking system requirements...")
        
        # Check Python modules
        required_modules = ['depthai', 'cv2', 'websockets', 'asyncio']
        for module in required_modules:
            try:
                __import__(module)
                logger.info(f"✅ {module} available")
            except ImportError:
                logger.error(f"❌ {module} not available - please install: pip install {module}")
                return False
        
        # Check if required files exist
        required_files = [
            'oak_camera_bridge.py',
            'websocket_server.py',
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
        """Monitor all processes"""
        while self.running:
            for name, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    logger.warning(f"⚠️ Process {name} exited with code {proc.returncode}")
                    
            time.sleep(5)
    
    def start_all_servers(self):
        """Start all available servers"""
        if not self.check_requirements():
            logger.error("❌ Requirements check failed")
            return False
        
        logger.info("🚀 Starting OAK camera server stack...")
        self.running = True
        
        # Start core servers
        servers = [
            ('OAK Camera Bridge', self.start_oak_camera_bridge),
            ('WebSocket Signaling Server', self.start_websocket_server),
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
        logger.info("   HTTP Client Server:      http://localhost:8000")
        logger.info("")
        logger.info("🎯 Open client: http://localhost:8000/clients/oak_websocket_client.html")
        logger.info("")
        logger.info("🔧 Available Streaming Technologies:")
        logger.info("  • WebCodecs: Hardware-accelerated, lowest latency (Chrome only)")
        logger.info("  • Canvas: Universal compatibility, all browsers")
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
    server = OAKServerManager()
    
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
