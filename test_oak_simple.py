#!/usr/bin/env python3
"""
Simple OAK Camera Test
"""

import depthai as dai
import sys

def test_oak_simple():
    """Simple OAK camera test"""
    print("🔍 Looking for OAK cameras...")
    
    try:
        # Try to get all devices
        devices = dai.Device.getAllAvailableDevices()
        print(f"Found {len(devices)} DepthAI devices")
        
        if len(devices) == 0:
            print("❌ No OAK cameras detected by DepthAI")
            print("Trying to create device directly...")
            
            # Try to create device directly
            try:
                with dai.Device() as device:
                    print("✅ Successfully connected to OAK camera!")
                    return True
            except Exception as e:
                print(f"❌ Failed to connect directly: {e}")
                return False
        else:
            print("✅ OAK cameras found:")
            for i, dev in enumerate(devices):
                print(f"  {i}: {dev.name} - {dev.mxid}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_oak_simple()
