#!/usr/bin/env python3
"""
Mock Hardware Module for WaterPlantOperator
Simulates Raspberry Pi hardware components in a container environment
"""

import os
import time
import random
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockGPIO:
    """Mock GPIO class to simulate Raspberry Pi GPIO operations"""
    
    # GPIO pin modes
    OUT = "out"
    IN = "in"
    
    # GPIO pin states
    HIGH = 1
    LOW = 0
    
    def __init__(self):
        self.pins = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for GPIO operations"""
        self.logger = logging.getLogger(f"{__name__}.GPIO")
    
    def setmode(self, mode):
        """Set GPIO numbering mode"""
        self.logger.info(f"GPIO mode set to: {mode}")
    
    def setwarnings(self, warnings):
        """Set GPIO warnings"""
        self.logger.info(f"GPIO warnings set to: {warnings}")
    
    def setup(self, pin, mode, initial=None):
        """Setup a GPIO pin"""
        self.pins[pin] = {
            'mode': mode,
            'state': initial if initial is not None else self.LOW
        }
        self.logger.info(f"GPIO pin {pin} setup as {mode}, initial: {initial}")
    
    def output(self, pin, state):
        """Set GPIO pin output"""
        if pin in self.pins:
            self.pins[pin]['state'] = state
            self.logger.info(f"GPIO pin {pin} set to {state}")
        else:
            self.logger.warning(f"GPIO pin {pin} not setup")
    
    def input(self, pin):
        """Read GPIO pin input"""
        if pin in self.pins:
            # Simulate some random input for testing
            if self.pins[pin]['mode'] == self.IN:
                return random.choice([self.HIGH, self.LOW])
            return self.pins[pin]['state']
        else:
            self.logger.warning(f"GPIO pin {pin} not setup")
            return self.LOW
    
    def cleanup(self):
        """Cleanup GPIO pins"""
        self.pins.clear()
        self.logger.info("GPIO cleanup completed")

class MockCamera:
    """Mock Camera class to simulate Raspberry Pi Camera operations"""
    
    def __init__(self):
        self.is_recording = False
        self.resolution = (1920, 1080)
        self.logger = logging.getLogger(f"{__name__}.Camera")
    
    def start_preview(self):
        """Start camera preview"""
        self.logger.info("Camera preview started")
    
    def stop_preview(self):
        """Stop camera preview"""
        self.logger.info("Camera preview stopped")
    
    def capture(self, output, format='jpeg'):
        """Capture image"""
        # Create a mock image file
        if isinstance(output, str):
            with open(output, 'wb') as f:
                # Write a minimal JPEG header
                f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
        self.logger.info(f"Image captured: {output}")
    
    def start_recording(self, output):
        """Start video recording"""
        self.is_recording = True
        self.logger.info(f"Video recording started: {output}")
    
    def stop_recording(self):
        """Stop video recording"""
        self.is_recording = False
        self.logger.info("Video recording stopped")
    
    def close(self):
        """Close camera"""
        self.logger.info("Camera closed")

class MockSensor:
    """Mock sensor class to simulate various sensors"""
    
    def __init__(self, sensor_type: str):
        self.sensor_type = sensor_type
        self.logger = logging.getLogger(f"{__name__}.Sensor.{sensor_type}")
    
    def read_moisture(self) -> float:
        """Read moisture sensor (0.0 to 1.0)"""
        # Simulate moisture reading
        moisture = random.uniform(0.1, 0.9)
        self.logger.info(f"Moisture sensor reading: {moisture:.2f}")
        return moisture
    
    def read_temperature(self) -> float:
        """Read temperature sensor in Celsius"""
        # Simulate temperature reading
        temperature = random.uniform(15.0, 35.0)
        self.logger.info(f"Temperature sensor reading: {temperature:.1f}°C")
        return temperature
    
    def read_humidity(self) -> float:
        """Read humidity sensor (0.0 to 1.0)"""
        # Simulate humidity reading
        humidity = random.uniform(0.3, 0.8)
        self.logger.info(f"Humidity sensor reading: {humidity:.2f}")
        return humidity
    
    def read_water_level(self) -> float:
        """Read water level sensor (0.0 to 1.0)"""
        # Simulate water level reading
        water_level = random.uniform(0.2, 1.0)
        self.logger.info(f"Water level sensor reading: {water_level:.2f}")
        return water_level

class MockRelay:
    """Mock relay class to simulate relay operations"""
    
    def __init__(self, pin: int):
        self.pin = pin
        self.state = False
        self.logger = logging.getLogger(f"{__name__}.Relay.{pin}")
    
    def on(self):
        """Turn relay on"""
        self.state = True
        self.logger.info(f"Relay {self.pin} turned ON")
    
    def off(self):
        """Turn relay off"""
        self.state = False
        self.logger.info(f"Relay {self.pin} turned OFF")
    
    def is_on(self) -> bool:
        """Check if relay is on"""
        return self.state

class MockHardwareManager:
    """Main hardware manager for mock hardware operations"""
    
    def __init__(self):
        self.gpio = MockGPIO()
        self.camera = MockCamera()
        self.sensors = {}
        self.relays = {}
        self.logger = logging.getLogger(f"{__name__}.HardwareManager")
        self.setup_hardware()
    
    def setup_hardware(self):
        """Setup mock hardware components"""
        self.logger.info("Setting up mock hardware components...")
        
        # Setup GPIO
        self.gpio.setmode("BCM")
        self.gpio.setwarnings(False)
        
        # Setup sensors
        self.sensors['moisture'] = MockSensor('moisture')
        self.sensors['temperature'] = MockSensor('temperature')
        self.sensors['humidity'] = MockSensor('humidity')
        self.sensors['water_level'] = MockSensor('water_level')
        
        # Setup relays
        self.relays['pump'] = MockRelay(18)
        self.relays['valve'] = MockRelay(19)
        self.relays['light'] = MockRelay(20)
        
        self.logger.info("Mock hardware setup completed")
    
    def get_sensor_reading(self, sensor_type: str) -> float:
        """Get reading from specified sensor"""
        if sensor_type in self.sensors:
            sensor = self.sensors[sensor_type]
            if sensor_type == 'moisture':
                return sensor.read_moisture()
            elif sensor_type == 'temperature':
                return sensor.read_temperature()
            elif sensor_type == 'humidity':
                return sensor.read_humidity()
            elif sensor_type == 'water_level':
                return sensor.read_water_level()
        else:
            self.logger.warning(f"Unknown sensor type: {sensor_type}")
            return 0.0
    
    def control_relay(self, relay_name: str, state: bool):
        """Control relay state"""
        if relay_name in self.relays:
            relay = self.relays[relay_name]
            if state:
                relay.on()
            else:
                relay.off()
        else:
            self.logger.warning(f"Unknown relay: {relay_name}")
    
    def take_photo(self, filename: str) -> bool:
        """Take a photo using mock camera"""
        try:
            self.camera.capture(filename)
            return True
        except Exception as e:
            self.logger.error(f"Failed to take photo: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get mock system information"""
        return {
            'timestamp': datetime.now().isoformat(),
            'environment': 'container',
            'simulation_mode': True,
            'sensors': {
                'moisture': self.get_sensor_reading('moisture'),
                'temperature': self.get_sensor_reading('temperature'),
                'humidity': self.get_sensor_reading('humidity'),
                'water_level': self.get_sensor_reading('water_level')
            },
            'relays': {
                name: relay.is_on() for name, relay in self.relays.items()
            },
            'camera': {
                'available': True,
                'recording': self.camera.is_recording
            }
        }
    
    def cleanup(self):
        """Cleanup hardware resources"""
        self.logger.info("Cleaning up mock hardware...")
        self.gpio.cleanup()
        self.camera.close()
        self.logger.info("Mock hardware cleanup completed")

# Global hardware manager instance
hardware_manager = MockHardwareManager()

# Export mock classes for compatibility
GPIO = MockGPIO
Camera = MockCamera
Sensor = MockSensor
Relay = MockRelay

def get_hardware_manager():
    """Get the global hardware manager instance"""
    return hardware_manager

if __name__ == "__main__":
    # Test the mock hardware
    print("Testing Mock Hardware...")
    
    # Test sensors
    print(f"Moisture: {hardware_manager.get_sensor_reading('moisture'):.2f}")
    print(f"Temperature: {hardware_manager.get_sensor_reading('temperature'):.1f}°C")
    print(f"Humidity: {hardware_manager.get_sensor_reading('humidity'):.2f}")
    print(f"Water Level: {hardware_manager.get_sensor_reading('water_level'):.2f}")
    
    # Test relays
    hardware_manager.control_relay('pump', True)
    hardware_manager.control_relay('valve', False)
    
    # Test camera
    hardware_manager.take_photo('/tmp/test_photo.jpg')
    
    # Test system info
    print("\nSystem Info:")
    import json
    print(json.dumps(hardware_manager.get_system_info(), indent=2))
    
    print("\nMock hardware test completed!")


