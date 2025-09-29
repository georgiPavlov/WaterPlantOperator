# WaterPlantOperator - Automated Plant Watering System

A comprehensive IoT-based plant watering automation system designed for Raspberry Pi with moisture sensing, scheduled watering, and remote monitoring capabilities.

## Table of Contents

1. [System Overview](#system-overview)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Dependencies](#software-dependencies)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Running the System](#running-the-system)
7. [Testing](#testing)
8. [System Architecture](#system-architecture)
9. [API Integration](#api-integration)
10. [Troubleshooting](#troubleshooting)
11. [Development Guide](#development-guide)

## System Overview

The WaterPlantOperator is an intelligent plant watering system that:

- **Monitors soil moisture** using capacitive moisture sensors
- **Schedules watering** based on time or moisture thresholds
- **Controls water pumps** via relay modules
- **Captures plant photos** using Raspberry Pi camera
- **Communicates with remote servers** for monitoring and control
- **Sends email notifications** for system status updates

### Key Features

- 🌱 **Moisture-based watering**: Automatically waters when soil moisture drops below threshold
- ⏰ **Time-based scheduling**: Water plants at specific times and days
- 📸 **Photo capture**: Take pictures of plants on demand
- 📊 **Remote monitoring**: Real-time status updates to web dashboard
- 📧 **Email notifications**: Get notified of watering events and system status
- 🔧 **Modular design**: Easy to extend and customize

## Hardware Requirements

### Essential Components

| Component | Purpose | Connection |
|-----------|---------|------------|
| **Raspberry Pi 4** (4GB+) | Main controller | - |
| **Capacitive Moisture Sensor** | Soil moisture detection | GPIO pins |
| **Relay Module** | Water pump control | GPIO pins |
| **Water Pump** (12V) | Water delivery | Via relay |
| **Raspberry Pi Camera** | Plant photography | Camera port |
| **Power Supply** | System power | 5V/3A for Pi, 12V for pump |

### Optional Components

| Component | Purpose | Connection |
|-----------|---------|------------|
| **Water Level Sensor** | Tank monitoring | GPIO pins |
| **LED Indicators** | Status display | GPIO pins |
| **Buzzer** | Audio alerts | GPIO pins |
| **LCD Display** | Local status | I2C/SPI |

### Wiring Diagram

```
Raspberry Pi 4 GPIO Connections:
├── GPIO 18 → Relay IN (Pump Control)
├── GPIO 24 → Moisture Sensor VCC
├── GPIO 25 → Moisture Sensor GND
├── GPIO 8  → Moisture Sensor Signal
├── GPIO 2  → Water Level Sensor (I2C SDA)
├── GPIO 3  → Water Level Sensor (I2C SCL)
└── 5V/3.3V → Power for sensors
```

## Software Dependencies

### System Requirements

- **Operating System**: Raspberry Pi OS (Bullseye or newer)
- **Python Version**: 3.9+
- **Memory**: 2GB+ RAM recommended
- **Storage**: 8GB+ SD card

### Python Packages

```bash
# Core dependencies
gpiozero>=1.6.2          # GPIO control
picamera>=1.13           # Camera interface
requests>=2.28.0         # HTTP communication
smtplib                  # Email sending (built-in)

# Development and testing
pytest>=7.0.0           # Testing framework
pytest-mock>=3.10.0     # Mocking utilities
pytest-cov>=4.0.0       # Coverage reporting
```

## Installation Guide

### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3-pip python3-venv git

# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options → Camera → Enable
```

### 2. Clone Repository

```bash
# Clone the project
git clone <repository-url>
cd WaterPlantOperator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install test dependencies (optional)
pip install -r requirements-test.txt
```

### 4. Hardware Setup

```bash
# Enable GPIO and I2C interfaces
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
# Navigate to: Interface Options → SPI → Enable

# Add user to gpio group
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER

# Reboot to apply changes
sudo reboot
```

## Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Server Configuration
SERVER_BASE_URL=https://your-server.com/api
SERVER_API_KEY=your-api-key-here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=recipient@example.com

# System Configuration
WATER_MAX_CAPACITY=3000
WATER_PUMP_RATE=10
MOISTURE_MAX_LEVEL=100
CYCLE_WAIT_TIME=60

# GPIO Pin Configuration
RELAY_PIN=18
MOISTURE_PIN=8
WATER_LEVEL_PIN=2
```

### 2. System Configuration

Edit `config/system_config.py`:

```python
# Pump Configuration
PUMP_CONFIG = {
    'water_max_capacity': 3000,  # ml
    'water_pumped_in_second': 10,  # ml/s
    'moisture_max_level': 100
}

# Timing Configuration
TIMING_CONFIG = {
    'wait_time_between_cycle': 60,  # seconds
    'photo_capture_timeout': 30,    # seconds
    'watering_timeout': 300         # seconds
}

# Sensor Configuration
SENSOR_CONFIG = {
    'moisture_threshold': 0.4,      # 40% moisture threshold
    'water_level_threshold': 0.2,   # 20% water level threshold
    'sensor_read_interval': 5       # seconds
}
```

## Running the System

### 1. Basic Startup

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main application
python3 run/main.py
```

### 2. Service Installation (Recommended)

Create a systemd service for automatic startup:

```bash
# Create service file
sudo nano /etc/systemd/system/waterplant.service
```

Add the following content:

```ini
[Unit]
Description=Water Plant Operator Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/WaterPlantOperator
Environment=PATH=/home/pi/WaterPlantOperator/venv/bin
ExecStart=/home/pi/WaterPlantOperator/venv/bin/python run/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable waterplant.service

# Start service
sudo systemctl start waterplant.service

# Check status
sudo systemctl status waterplant.service
```

### 3. Manual Control

```bash
# Check system status
python3 -c "from run.operation.server_checker import ServerChecker; print('System ready')"

# Test individual components
python3 -c "from run.operation.pump import Pump; p = Pump(3000, 10, 100); print('Pump initialized')"

# Test sensors
python3 -c "from run.sensor.moisture_sensor import Moisture; m = Moisture(8); print(f'Moisture: {m.value}')"
```

## Testing

### 1. Unit Tests

```bash
# Run all unit tests
python3 run_tests.py unit

# Run specific test categories
python3 -m pytest tests/unit/model/ -v
python3 -m pytest tests/unit/operation/ -v
python3 -m pytest tests/unit/communication/ -v

# Run with coverage
python3 -m pytest tests/unit/ --cov=run --cov-report=html
```

### 2. Integration Tests

```bash
# Run integration tests (requires hardware)
python3 run_tests.py integration

# Run specific integration tests
python3 -m pytest tests/integration/test_water_plant_workflow.py -v
python3 -m pytest tests/integration/test_edge_cases.py -v
```

### 3. Hardware Tests

```bash
# Test GPIO functionality
python3 -c "
from gpiozero import LED, Button
led = LED(18)
led.on()
print('GPIO test: LED should be on')
"

# Test camera
python3 -c "
from picamera import PiCamera
camera = PiCamera()
camera.capture('test_image.jpg')
print('Camera test: Image captured')
"

# Test moisture sensor
python3 -c "
from run.sensor.moisture_sensor import Moisture
sensor = Moisture(8)
print(f'Moisture reading: {sensor.value}')
"
```

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    WaterPlantOperator                       │
├─────────────────────────────────────────────────────────────┤
│  Main Application (main.py)                                │
│  ├── ServerChecker (Main Loop)                             │
│  ├── Pump (Watering Logic)                                 │
│  ├── ServerCommunicator (API Client)                       │
│  └── EmailSender (Notifications)                           │
├─────────────────────────────────────────────────────────────┤
│  Models (Data Structures)                                  │
│  ├── Plan (Basic Watering Plan)                            │
│  ├── MoisturePlan (Moisture-based Plan)                    │
│  ├── TimePlan (Scheduled Plan)                             │
│  ├── Status (Operation Results)                            │
│  └── Device (Device Information)                           │
├─────────────────────────────────────────────────────────────┤
│  Sensors & Hardware                                        │
│  ├── MoistureSensor (Soil Moisture)                        │
│  ├── Relay (Pump Control)                                  │
│  ├── Camera (Plant Photography)                            │
│  └── WaterLevelSensor (Tank Monitoring)                    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. ServerChecker starts main loop
2. Checks server for new plans/commands
3. Updates water level if needed
4. Captures photos if requested
5. Executes watering plans based on:
   - Moisture levels
   - Scheduled times
   - Manual commands
6. Sends results back to server
7. Waits for next cycle
```

### Plan Types

#### 1. Basic Plan
```json
{
  "name": "daily_watering",
  "plan_type": "basic",
  "water_volume": 200
}
```

#### 2. Moisture Plan
```json
{
  "name": "smart_watering",
  "plan_type": "moisture",
  "water_volume": 150,
  "moisture_threshold": 0.4,
  "check_interval": 30
}
```

#### 3. Time Plan
```json
{
  "name": "scheduled_watering",
  "plan_type": "time_based",
  "water_volume": 180,
  "weekday_times": [
    {"weekday": "Monday", "time_water": "08:00"},
    {"weekday": "Wednesday", "time_water": "08:00"},
    {"weekday": "Friday", "time_water": "08:00"}
  ],
  "execute_only_once": false
}
```

## API Integration

### Server Endpoints

The system communicates with a remote server using REST API:

#### 1. Health Check
```http
POST /api/plan-execution
Content-Type: application/json

{
  "watering_status": false,
  "message": "healthcheck"
}
```

#### 2. Get Watering Plan
```http
GET /api/plan
Authorization: Bearer <api-key>
```

#### 3. Post Execution Results
```http
POST /api/plan-execution
Content-Type: application/json
Authorization: Bearer <api-key>

{
  "watering_status": true,
  "message": "[Plant successfully watered with moisture plan]"
}
```

#### 4. Post Water Level
```http
POST /api/water
Content-Type: application/json
Authorization: Bearer <api-key>

{
  "water_level": 85.5
}
```

#### 5. Post Moisture Level
```http
POST /api/moisture
Content-Type: application/json
Authorization: Bearer <api-key>

{
  "moisture_level": 45
}
```

#### 6. Get Photo Request
```http
GET /api/picture
Authorization: Bearer <api-key>
```

#### 7. Post Photo
```http
POST /api/picture
Content-Type: multipart/form-data
Authorization: Bearer <api-key>

{
  "photo": <image-file>,
  "filename": "plant_20231201_143022.jpg"
}
```

### Server Requirements

Your server should implement these endpoints:

```python
# Example Flask server structure
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/api/plan', methods=['GET'])
def get_plan():
    # Return watering plan or empty JSON
    return jsonify({})  # No plan
    # or return jsonify({"name": "test", "plan_type": "basic", "water_volume": 200})

@app.route('/api/plan-execution', methods=['POST'])
def post_plan_execution():
    data = request.json
    # Process execution results
    print(f"Execution result: {data}")
    return jsonify({"status": "received"})

@app.route('/api/water', methods=['POST'])
def post_water():
    data = request.json
    # Process water level update
    print(f"Water level: {data['water_level']}%")
    return jsonify({"status": "received"})

@app.route('/api/moisture', methods=['POST'])
def post_moisture():
    data = request.json
    # Process moisture level update
    print(f"Moisture level: {data['moisture_level']}%")
    return jsonify({"status": "received"})

@app.route('/api/picture', methods=['GET'])
def get_picture_request():
    # Return photo request or empty JSON
    return jsonify({})  # No photo request
    # or return jsonify({"photo_id": "plant_photo_001"})

@app.route('/api/picture', methods=['POST'])
def post_picture():
    # Handle uploaded photo
    photo = request.files['photo']
    filename = request.form['filename']
    photo.save(f"uploads/{filename}")
    return jsonify({"status": "received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Troubleshooting

### Common Issues

#### 1. GPIO Permission Errors
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo reboot
```

#### 2. Camera Not Found
```bash
# Enable camera interface
sudo raspi-config
# Interface Options → Camera → Enable
sudo reboot

# Test camera
python3 -c "from picamera import PiCamera; PiCamera().capture('test.jpg')"
```

#### 3. Network Connection Issues
```bash
# Check network connectivity
ping google.com

# Check DNS resolution
nslookup your-server.com

# Test API connectivity
curl -X GET https://your-server.com/api/plan
```

#### 4. Sensor Reading Issues
```bash
# Check GPIO pins
gpio readall

# Test individual sensors
python3 -c "
from run.sensor.moisture_sensor import Moisture
sensor = Moisture(8)
print(f'Moisture: {sensor.value}')
"
```

#### 5. Pump Not Working
```bash
# Check relay connections
python3 -c "
from gpiozero import LED
relay = LED(18)
relay.on()  # Should activate pump
print('Pump should be running')
"

# Check power supply
# Ensure 12V supply is connected to pump
```

### Log Analysis

```bash
# View system logs
sudo journalctl -u waterplant.service -f

# View application logs
tail -f /home/pi/WaterPlantOperator/logs/waterplant.log

# Check system resources
htop
df -h
free -h
```

### Performance Monitoring

```bash
# Monitor system performance
watch -n 1 'echo "CPU: $(cat /proc/loadavg)"; echo "Memory: $(free -h | grep Mem)"; echo "Disk: $(df -h / | tail -1)"'

# Monitor network
iftop

# Monitor GPIO
gpio readall
```

## Development Guide

### Project Structure

```
WaterPlantOperator/
├── run/                          # Main application code
│   ├── main.py                  # Application entry point
│   ├── model/                   # Data models
│   │   ├── plan.py             # Base plan class
│   │   ├── moisture_plan.py    # Moisture-based plans
│   │   ├── time_plan.py        # Time-based plans
│   │   ├── status.py           # Operation status
│   │   └── device.py           # Device information
│   ├── operation/              # Core business logic
│   │   ├── pump.py            # Watering operations
│   │   ├── server_checker.py  # Main execution loop
│   │   └── camera_op.py       # Camera operations
│   ├── sensor/                 # Hardware interfaces
│   │   ├── moisture_sensor.py # Moisture sensor
│   │   ├── relay.py           # Relay control
│   │   └── camera_sensor.py   # Camera interface
│   ├── communication/          # External communication
│   │   ├── server_communicator.py # API client
│   │   └── email_sender.py    # Email notifications
│   └── common/                 # Utilities
│       ├── json_creator.py    # JSON handling
│       ├── time_keeper.py     # Time management
│       └── file.py            # File operations
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── conftest.py           # Test configuration
├── docs/                      # Documentation
├── config/                    # Configuration files
├── logs/                      # Log files
└── requirements.txt           # Dependencies
```

### Adding New Features

#### 1. New Sensor Type
```python
# Create new sensor class
class TemperatureSensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = DS18B20()
    
    @property
    def value(self):
        return self.sensor.temperature
```

#### 2. New Plan Type
```python
# Extend base Plan class
class TemperaturePlan(Plan):
    def __init__(self, name, plan_type, water_volume, temperature_threshold):
        super().__init__(name, plan_type, water_volume)
        self.temperature_threshold = temperature_threshold
```

#### 3. New Communication Method
```python
# Add new communication class
class MQTTCommunicator:
    def __init__(self, broker_url, topic):
        self.broker_url = broker_url
        self.topic = topic
        self.client = mqtt.Client()
    
    def publish_status(self, status):
        self.client.publish(f"{self.topic}/status", status)
```

### Testing New Features

```bash
# Create test file
touch tests/unit/sensor/test_temperature_sensor.py

# Write tests
cat > tests/unit/sensor/test_temperature_sensor.py << 'EOF'
import pytest
from run.sensor.temperature_sensor import TemperatureSensor

class TestTemperatureSensor:
    def test_temperature_reading(self):
        sensor = TemperatureSensor(4)
        temp = sensor.value
        assert isinstance(temp, float)
        assert 0 <= temp <= 50  # Reasonable temperature range
EOF

# Run tests
python3 -m pytest tests/unit/sensor/test_temperature_sensor.py -v
```

### Code Quality

```bash
# Run linting
python3 -m flake8 run/
python3 -m black run/
python3 -m isort run/

# Run type checking
python3 -m mypy run/

# Run security checks
python3 -m bandit -r run/
```

---

## Support and Contributing

### Getting Help

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and feature requests via GitHub issues
- **Discussions**: Join community discussions for questions and ideas

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Plant Watering! 🌱💧**
