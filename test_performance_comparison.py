#!/usr/bin/env python3
"""
Performance Comparison Test for WebCodecs vs Canvas
"""

import time
import asyncio
import websockets
import json

async def performance_test():
    print("🧪 WebCodecs vs Canvas Performance Test")
    print("=" * 50)
    
    print("📋 Test Instructions:")
    print("1. Start servers: python start_oak_servers.py")
    print("2. Open Chrome (for WebCodecs support): http://localhost:5001/oak")
    print("3. Connect to server and OAK camera")
    print("4. Start video streaming")
    print("5. Click '📊 Performance Report' button every 10 seconds")
    print("6. Compare the results!")
    
    print("\n🔍 What to Look For:")
    print("• WebCodecs: Lower processing times (< 5ms typical)")
    print("• Canvas: Higher processing times (> 10ms typical)")
    print("• Memory usage differences")
    print("• Frame rate stability")
    
    print("\n💡 Expected Results:")
    print("• WebCodecs: ~2-5ms per frame, lower memory usage")
    print("• Canvas: ~10-20ms per frame, higher memory usage")
    print("• WebCodecs should feel more responsive")

if __name__ == "__main__":
    asyncio.run(performance_test())
