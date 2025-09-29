#!/usr/bin/env python3
"""
Test script for WaterPlantOperator container setup
Tests the container configuration and hardware simulation
"""

import sys
import os
import json
from datetime import datetime

# Add the run directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'run'))

def test_mock_hardware():
    """Test the mock hardware functionality"""
    print("🧪 Testing Mock Hardware...")
    
    try:
        from mock_hardware import MockHardwareManager, get_hardware_manager
        
        # Get hardware manager
        hw_manager = get_hardware_manager()
        
        # Test sensor readings
        print("\n📊 Sensor Readings:")
        sensors = ['moisture', 'temperature', 'humidity', 'water_level']
        for sensor in sensors:
            reading = hw_manager.get_sensor_reading(sensor)
            print(f"  {sensor}: {reading}")
        
        # Test relay control
        print("\n🔌 Relay Control:")
        relays = ['pump', 'valve', 'light']
        for relay in relays:
            hw_manager.control_relay(relay, True)
            print(f"  {relay}: ON")
            hw_manager.control_relay(relay, False)
            print(f"  {relay}: OFF")
        
        # Test camera
        print("\n📷 Camera Test:")
        photo_success = hw_manager.take_photo('/tmp/test_photo.jpg')
        print(f"  Photo capture: {'✅ Success' if photo_success else '❌ Failed'}")
        
        # Test system info
        print("\n💻 System Information:")
        system_info = hw_manager.get_system_info()
        print(json.dumps(system_info, indent=2))
        
        print("\n✅ Mock hardware test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Mock hardware test failed: {e}")
        return False

def test_container_config():
    """Test the container configuration"""
    print("\n🔧 Testing Container Configuration...")
    
    try:
        from config.container_config import get_config
        
        config = get_config()
        
        print(f"  Environment: {config.environment}")
        print(f"  Simulation Mode: {config.simulation_mode}")
        print(f"  API Host: {config.api_host}")
        print(f"  API Port: {config.api_port}")
        print(f"  Backend URL: {config.backend_url}")
        print(f"  Mock GPIO: {config.mock_gpio}")
        print(f"  Mock Camera: {config.mock_camera}")
        print(f"  Mock Sensors: {config.mock_sensors}")
        
        print("\n✅ Container configuration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Container configuration test failed: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'requests',
        'psutil',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All dependencies are available!")
        return True

def test_environment():
    """Test environment setup"""
    print("\n🌍 Testing Environment...")
    
    # Check environment variables
    env_vars = [
        'ENVIRONMENT',
        'SIMULATION_MODE',
        'LOG_LEVEL',
        'API_HOST',
        'API_PORT'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'Not set')
        print(f"  {var}: {value}")
    
    # Check directories
    directories = ['logs', 'data', 'config', 'monitoring']
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/ directory exists")
        else:
            print(f"  ❌ {directory}/ directory missing")
    
    print("\n✅ Environment test completed!")
    return True

def main():
    """Main test function"""
    print("🐳 WaterPlantOperator Container Test Suite")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_environment,
        test_container_config,
        test_mock_hardware
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Container is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
