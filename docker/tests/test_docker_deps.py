#!/usr/bin/env python3
"""
Docker Dependency Test Script

Tests that all required Python modules are available in the Docker container.
"""

import sys
import importlib


def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name} ({package_name}) - AVAILABLE")
            return True
        else:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name} - AVAILABLE")
            return True
    except ImportError as e:
        print(f"❌ {module_name} - NOT AVAILABLE: {e}")
        return False


def main():
    """Test all required modules"""
    print("🐍 Testing Python dependencies in Docker container...")
    print("=" * 60)

    # Test all required modules
    required_modules = [('websockets', 'websockets'), ('depthai', 'depthai'),
                        ('cv2', 'opencv-python'), ('flask', 'Flask'),
                        ('asyncio', 'built-in'), ('json', 'built-in'),
                        ('threading', 'built-in'), ('subprocess', 'built-in'),
                        ('pathlib', 'built-in'), ('numpy', 'numpy'),
                        ('PIL', 'Pillow')]

    success_count = 0
    total_count = len(required_modules)

    for module_name, package_name in required_modules:
        if test_import(module_name, package_name):
            success_count += 1

    print("=" * 60)
    print(f"📊 Results: {success_count}/{total_count} modules available")

    if success_count == total_count:
        print("🎉 All dependencies are available!")
        return 0
    else:
        print("❌ Some dependencies are missing!")
        print("💡 Try running: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
