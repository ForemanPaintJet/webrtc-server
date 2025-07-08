#!/usr/bin/env python3
"""
OAK Camera Docker Test Script

Quick test to check if OAK cameras are accessible in Docker container.
"""

import sys

def test_oak_camera_detection():
    """Test OAK camera detection in Docker"""
    print("🔶 Testing OAK Camera Detection in Docker Container")
    print("=" * 55)
    
    try:
        import depthai as dai
        print("✅ DepthAI library imported successfully")
        
        # Test device detection
        print("🔍 Scanning for OAK devices...")
        devices = dai.Device.getAllAvailableDevices()
        
        if len(devices) == 0:
            print("⚠️  No OAK devices found via getAllAvailableDevices()")
            
            # Try direct connection
            print("🔄 Attempting direct device connection...")
            try:
                with dai.Device() as device:
                    print("✅ OAK camera connected directly!")
                    print(f"   Device info: {device.getDeviceInfo()}")
                    return True
            except Exception as e:
                print(f"❌ Direct connection failed: {e}")
                print()
                print("💡 Troubleshooting:")
                print("   1. Ensure OAK camera is connected to host")
                print("   2. Check host detection: lsusb | grep -i movidius")
                print("   3. Run container with: --privileged -v /dev:/dev")
                print("   4. Or use: --device=/dev/bus/usb")
                return False
        else:
            print(f"✅ Found {len(devices)} OAK device(s):")
            for i, device in enumerate(devices):
                print(f"   📷 Device {i}: {device.name} ({device.mxid})")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import depthai: {e}")
        print("💡 Install with: pip install depthai")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_usb_access():
    """Test USB device access"""
    print("\n🔌 Testing USB Device Access")
    print("=" * 30)
    
    import os
    import subprocess
    
    # Check if /dev/bus/usb exists
    if os.path.exists("/dev/bus/usb"):
        print("✅ /dev/bus/usb directory exists")
        
        # Try to list USB devices
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ lsusb command successful")
                
                # Check for Movidius devices
                if 'movidius' in result.stdout.lower():
                    print("🎯 Movidius device detected in lsusb!")
                    print("   OAK camera should be accessible")
                else:
                    print("⚠️  No Movidius devices in lsusb output")
                    print("   Check if OAK camera is connected to host")
            else:
                print(f"⚠️  lsusb failed with code {result.returncode}")
        except subprocess.TimeoutExpired:
            print("⚠️  lsusb command timed out")
        except FileNotFoundError:
            print("⚠️  lsusb command not found")
    else:
        print("❌ /dev/bus/usb not accessible")
        print("💡 Run container with: --device=/dev/bus/usb")

def main():
    """Main test function"""
    print("🐳 OAK Camera Docker Compatibility Test")
    print("=" * 40)
    
    # Test USB access first
    test_usb_access()
    
    # Test OAK camera detection
    oak_success = test_oak_camera_detection()
    
    print("\n📊 Test Results Summary")
    print("=" * 25)
    
    if oak_success:
        print("🎉 OAK camera is accessible in Docker!")
        print("✅ oak_camera_bridge.py should work properly")
    else:
        print("⚠️  OAK camera not accessible in Docker")
        print("🔄 oak_camera_bridge.py will run in 'no camera' mode")
        print("\n💡 To fix:")
        print("   docker run --privileged -v /dev:/dev ...")
    
    return 0 if oak_success else 1

if __name__ == "__main__":
    sys.exit(main())
