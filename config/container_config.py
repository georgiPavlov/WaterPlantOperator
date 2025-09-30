#!/usr/bin/env python3
"""
Container Configuration for WaterPlantOperator
Configuration settings for running in a Podman container
"""

import os
from typing import Dict, Any

class ContainerConfig:
    """Configuration class for container environment"""
    
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'container')
        self.simulation_mode = os.getenv('SIMULATION_MODE', 'true').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # API Configuration
        self.api_host = os.getenv('API_HOST', '0.0.0.0')
        self.api_port = int(os.getenv('API_PORT', '8000'))
        
        # Backend Communication
        self.backend_url = os.getenv('BACKEND_URL', 'http://host.docker.internal:8001')
        self.backend_api_key = os.getenv('BACKEND_API_KEY', 'your-api-key-here')
        
        # Hardware Simulation Settings
        self.mock_gpio = os.getenv('MOCK_GPIO', 'true').lower() == 'true'
        self.mock_camera = os.getenv('MOCK_CAMERA', 'true').lower() == 'true'
        self.mock_sensors = os.getenv('MOCK_SENSORS', 'true').lower() == 'true'
        
        # File Paths
        self.logs_dir = '/app/logs'
        self.data_dir = '/app/data'
        self.config_dir = '/app/config'
        
        # GPIO Configuration
        self.gpio_pins = {
            'pump': 18,
            'valve': 19,
            'light': 20,
            'moisture_sensor': 21,
            'water_level_sensor': 22
        }
        
        # Camera Configuration
        self.camera_config = {
            'resolution': (1920, 1080),
            'format': 'jpeg',
            'quality': 85
        }
        
        # Sensor Configuration
        self.sensor_config = {
            'moisture': {
                'pin': 21,
                'threshold': 0.3,
                'read_interval': 30  # seconds
            },
            'water_level': {
                'pin': 22,
                'threshold': 0.2,
                'read_interval': 60  # seconds
            },
            'temperature': {
                'pin': 23,
                'threshold': 25.0,  # Celsius
                'read_interval': 120  # seconds
            }
        }
        
        # Pump Configuration
        self.pump_config = {
            'pin': 18,
            'max_runtime': 300,  # seconds
            'cooldown_time': 60,  # seconds
            'flow_rate': 1.0  # liters per minute
        }
        
        # Watering Plan Configuration
        self.watering_config = {
            'default_volume': 500,  # ml
            'max_volume': 2000,  # ml
            'min_interval': 3600,  # seconds (1 hour)
            'max_daily_waterings': 5
        }
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            'environment': self.environment,
            'simulation_mode': self.simulation_mode,
            'log_level': self.log_level,
            'api': {
                'host': self.api_host,
                'port': self.api_port
            },
            'backend': {
                'url': self.backend_url,
                'api_key': self.backend_api_key
            },
            'hardware': {
                'mock_gpio': self.mock_gpio,
                'mock_camera': self.mock_camera,
                'mock_sensors': self.mock_sensors
            },
            'gpio_pins': self.gpio_pins,
            'camera': self.camera_config,
            'sensors': self.sensor_config,
            'pump': self.pump_config,
            'watering': self.watering_config
        }
    
    def is_simulation_mode(self) -> bool:
        """Check if running in simulation mode"""
        return self.simulation_mode
    
    def is_container_environment(self) -> bool:
        """Check if running in container environment"""
        return self.environment == 'container'

# Global configuration instance
config = ContainerConfig()

def get_config() -> ContainerConfig:
    """Get the global configuration instance"""
    return config

if __name__ == "__main__":
    # Print configuration for debugging
    import json
    print("Container Configuration:")
    print(json.dumps(config.get_config_dict(), indent=2))


