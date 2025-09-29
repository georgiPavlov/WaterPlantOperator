"""
WaterPlantOperator System Configuration Example

Copy this file to system_config.py and modify the values according to your setup.
"""

# =============================================================================
# PUMP CONFIGURATION
# =============================================================================

PUMP_CONFIG = {
    # Maximum water capacity in milliliters
    'water_max_capacity': 3000,
    
    # Water pumping rate in milliliters per second
    'water_pumped_in_second': 10,
    
    # Maximum moisture level for sensor calibration
    'moisture_max_level': 100,
    
    # Extra time added after water reset for system stabilization (seconds)
    'water_reset_stabilization_time': 3
}

# =============================================================================
# TIMING CONFIGURATION
# =============================================================================

TIMING_CONFIG = {
    # Wait time between execution cycles (seconds)
    'wait_time_between_cycle': 60,
    
    # Photo capture timeout (seconds)
    'photo_capture_timeout': 30,
    
    # Watering operation timeout (seconds)
    'watering_timeout': 300,
    
    # Sensor reading interval (seconds)
    'sensor_read_interval': 5,
    
    # Health check interval (seconds)
    'health_check_interval': 30
}

# =============================================================================
# SENSOR CONFIGURATION
# =============================================================================

SENSOR_CONFIG = {
    # Moisture threshold for watering (0.0-1.0, where 0.4 = 40%)
    'moisture_threshold': 0.4,
    
    # Water level threshold for low water warning (0.0-1.0)
    'water_level_threshold': 0.2,
    
    # Temperature threshold for temperature-based watering (Celsius)
    'temperature_threshold': 25.0,
    
    # Light threshold for light-based watering (lux)
    'light_threshold': 1000
}

# =============================================================================
# GPIO PIN CONFIGURATION
# =============================================================================

GPIO_CONFIG = {
    # Relay control pin for water pump
    'relay_pin': 18,
    
    # Moisture sensor signal pin
    'moisture_sensor_pin': 8,
    
    # Water level sensor pin (I2C)
    'water_level_sensor_pin': 2,
    
    # LED indicator pins
    'status_led_pin': 21,
    'error_led_pin': 20,
    
    # Buzzer pin for audio alerts
    'buzzer_pin': 16,
    
    # Button pins for manual control
    'manual_water_button_pin': 23,
    'emergency_stop_button_pin': 24
}

# =============================================================================
# SERVER COMMUNICATION CONFIGURATION
# =============================================================================

SERVER_CONFIG = {
    # Base URL of your server API
    'base_url': 'https://your-server.com/api',
    
    # API key for authentication
    'api_key': 'your-api-key-here',
    
    # Request timeout (seconds)
    'request_timeout': 30,
    
    # Retry attempts for failed requests
    'retry_attempts': 3,
    
    # Retry delay between attempts (seconds)
    'retry_delay': 5,
    
    # SSL verification (True for production, False for self-signed certs)
    'verify_ssl': True
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_CONFIG = {
    # SMTP server settings
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    
    # Email credentials
    'email_user': 'your-email@gmail.com',
    'email_password': 'your-app-password',  # Use app password for Gmail
    
    # Recipients
    'recipients': [
        'admin@example.com',
        'user@example.com'
    ],
    
    # Email settings
    'use_tls': True,
    'use_ssl': False,
    
    # Email templates
    'templates': {
        'watering_success': 'Plant watered successfully at {time}',
        'watering_failure': 'Watering failed: {error}',
        'low_water': 'Water level is low: {level}%',
        'system_error': 'System error: {error}',
        'health_check': 'System health check: {status}'
    }
}

# =============================================================================
# CAMERA CONFIGURATION
# =============================================================================

CAMERA_CONFIG = {
    # Camera resolution
    'resolution': (1920, 1080),
    
    # Image quality (1-100)
    'quality': 85,
    
    # Photo storage directory
    'photo_directory': '/home/pi/WaterPlantOperator/photos',
    
    # Maximum number of photos to keep
    'max_photos': 100,
    
    # Photo naming format
    'photo_name_format': 'plant_{timestamp}.jpg',
    
    # Camera rotation (0, 90, 180, 270)
    'rotation': 0,
    
    # Camera brightness (0-100)
    'brightness': 50,
    
    # Camera contrast (-100 to 100)
    'contrast': 0
}

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_CONFIG = {
    # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    'level': 'INFO',
    
    # Log file path
    'log_file': '/home/pi/WaterPlantOperator/logs/waterplant.log',
    
    # Maximum log file size (MB)
    'max_file_size': 10,
    
    # Number of backup log files to keep
    'backup_count': 5,
    
    # Log format
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
    # Date format
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# =============================================================================
# PLANT-SPECIFIC CONFIGURATION
# =============================================================================

PLANT_CONFIG = {
    # Default watering plans for different plant types
    'plant_types': {
        'succulent': {
            'moisture_threshold': 0.2,
            'water_volume': 100,
            'check_interval': 60
        },
        'herb': {
            'moisture_threshold': 0.4,
            'water_volume': 150,
            'check_interval': 30
        },
        'vegetable': {
            'moisture_threshold': 0.5,
            'water_volume': 200,
            'check_interval': 20
        },
        'flower': {
            'moisture_threshold': 0.6,
            'water_volume': 180,
            'check_interval': 25
        }
    },
    
    # Default time-based schedules
    'default_schedules': {
        'morning': ['08:00'],
        'evening': ['18:00'],
        'twice_daily': ['08:00', '18:00'],
        'weekdays': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'weekends': ['Saturday', 'Sunday']
    }
}

# =============================================================================
# SAFETY CONFIGURATION
# =============================================================================

SAFETY_CONFIG = {
    # Maximum watering duration (seconds)
    'max_watering_duration': 300,
    
    # Maximum daily watering amount (ml)
    'max_daily_water': 1000,
    
    # Emergency stop enabled
    'emergency_stop_enabled': True,
    
    # Water level monitoring enabled
    'water_level_monitoring': True,
    
    # Overwatering protection
    'overwatering_protection': True,
    
    # Minimum time between waterings (minutes)
    'min_time_between_waterings': 30
}

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

DEVELOPMENT_CONFIG = {
    # Debug mode (enables additional logging)
    'debug_mode': False,
    
    # Test mode (uses mock sensors)
    'test_mode': False,
    
    # Simulation mode (no actual hardware control)
    'simulation_mode': False,
    
    # Performance monitoring
    'performance_monitoring': True,
    
    # Memory usage monitoring
    'memory_monitoring': True
}

# =============================================================================
# ENVIRONMENT-SPECIFIC OVERRIDES
# =============================================================================

# Override settings based on environment
import os

# Production environment
if os.getenv('ENVIRONMENT') == 'production':
    LOGGING_CONFIG['level'] = 'WARNING'
    SERVER_CONFIG['verify_ssl'] = True
    DEVELOPMENT_CONFIG['debug_mode'] = False

# Development environment
elif os.getenv('ENVIRONMENT') == 'development':
    LOGGING_CONFIG['level'] = 'DEBUG'
    SERVER_CONFIG['verify_ssl'] = False
    DEVELOPMENT_CONFIG['debug_mode'] = True

# Test environment
elif os.getenv('ENVIRONMENT') == 'test':
    DEVELOPMENT_CONFIG['test_mode'] = True
    DEVELOPMENT_CONFIG['simulation_mode'] = True
    TIMING_CONFIG['wait_time_between_cycle'] = 5
