# WaterPlantOperator - Quick Start Guide

Get your automated plant watering system up and running on Raspberry Pi in 30 minutes!

## 🚀 Quick Setup (30 minutes)

### Step 1: Hardware Setup (10 minutes)

**Required Components:**
- Raspberry Pi 4 (4GB+)
- MicroSD card (16GB+)
- Capacitive moisture sensor
- 12V water pump
- Relay module
- Raspberry Pi camera
- Power supplies (5V for Pi, 12V for pump)

**Wiring:**
```
Raspberry Pi → Hardware
├── GPIO 18 → Relay IN
├── GPIO 8  → Moisture Sensor Signal
├── 5V      → Moisture Sensor VCC
├── GND     → Moisture Sensor GND
└── Camera Port → Pi Camera
```

### Step 2: Software Installation (10 minutes)

```bash
# 1. Flash Raspberry Pi OS to SD card
# 2. Enable SSH and WiFi on first boot
# 3. SSH into your Pi

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv git

# Enable camera and GPIO
sudo raspi-config
# Interface Options → Camera → Enable
# Interface Options → I2C → Enable
# Interface Options → SPI → Enable

# Clone and setup project
git clone <your-repo-url>
cd WaterPlantOperator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configuration (5 minutes)

```bash
# Create configuration file
cp config/system_config.example.py config/system_config.py

# Edit configuration
nano config/system_config.py
```

**Basic Configuration:**
```python
# config/system_config.py
PUMP_CONFIG = {
    'water_max_capacity': 3000,  # ml
    'water_pumped_in_second': 10,  # ml/s
    'moisture_max_level': 100
}

SERVER_CONFIG = {
    'base_url': 'https://your-server.com/api',
    'api_key': 'your-api-key'
}

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_user': 'your-email@gmail.com',
    'email_password': 'your-app-password'
}
```

### Step 4: Test and Run (5 minutes)

```bash
# Test hardware
python3 -c "
from run.sensor.moisture_sensor import Moisture
from run.operation.pump import Pump
print('Hardware test: OK')
"

# Run the system
python3 run/main.py
```

## 🧪 Testing Your Setup

### Hardware Tests

```bash
# Test moisture sensor
python3 -c "
from run.sensor.moisture_sensor import Moisture
sensor = Moisture(8)
print(f'Moisture: {sensor.value:.2f}')
"

# Test pump relay
python3 -c "
from gpiozero import LED
relay = LED(18)
relay.on()
print('Pump should be running now')
input('Press Enter to stop...')
relay.off()
"

# Test camera
python3 -c "
from picamera import PiCamera
camera = PiCamera()
camera.capture('test_photo.jpg')
print('Photo captured: test_photo.jpg')
"
```

### System Tests

```bash
# Run unit tests
python3 run_tests.py unit

# Run integration tests
python3 run_tests.py integration
```

## 📱 Basic Usage

### 1. Manual Watering

```python
# Create a basic watering plan
from run.model.plan import Plan
from run.operation.pump import Pump

plan = Plan("manual_watering", "basic", 200)  # 200ml
pump = Pump(3000, 10, 100)
relay = LED(18)  # Your relay pin

# Execute watering
status = pump.execute_water_plan(plan, relay=relay)
print(f"Watering result: {status}")
```

### 2. Moisture-Based Watering

```python
# Create moisture plan
from run.model.moisture_plan import MoisturePlan

moisture_plan = MoisturePlan(
    name="smart_watering",
    plan_type="moisture",
    water_volume=150,
    moisture_threshold=0.4,  # 40% moisture threshold
    check_interval=30        # Check every 30 minutes
)

# Execute with moisture sensor
from run.sensor.moisture_sensor import Moisture
moisture_sensor = Moisture(8)

status = pump.execute_water_plan(moisture_plan, 
                                relay=relay, 
                                moisture_sensor=moisture_sensor)
```

### 3. Scheduled Watering

```python
# Create time-based plan
from run.model.time_plan import TimePlan
from run.model.watertime import WaterTime

# Water every Monday, Wednesday, Friday at 8:00 AM
watering_times = [
    WaterTime("Monday", "08:00"),
    WaterTime("Wednesday", "08:00"),
    WaterTime("Friday", "08:00")
]

time_plan = TimePlan(
    name="scheduled_watering",
    plan_type="time_based",
    water_volume=180,
    weekday_times=watering_times,
    execute_only_once=False
)

status = pump.execute_water_plan(time_plan, relay=relay)
```

## 🔧 Troubleshooting

### Common Issues

**Problem: "Permission denied" errors**
```bash
# Fix GPIO permissions
sudo usermod -a -G gpio $USER
sudo reboot
```

**Problem: Camera not found**
```bash
# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable
sudo reboot
```

**Problem: Moisture sensor reads 0**
```bash
# Check wiring
# Ensure sensor is connected to GPIO 8
# Check power supply (5V and GND)
```

**Problem: Pump doesn't work**
```bash
# Check relay connections
# Ensure 12V power supply to pump
# Test relay manually
```

### Getting Help

1. **Check logs**: `tail -f logs/waterplant.log`
2. **Run diagnostics**: `python3 run_tests.py unit`
3. **Test hardware**: Use the hardware test commands above
4. **Check connections**: Verify all wiring matches the diagram

## 🎯 Next Steps

Once your basic setup is working:

1. **Set up remote monitoring** - Configure server communication
2. **Add email notifications** - Get alerts for watering events
3. **Create custom plans** - Design watering schedules for your plants
4. **Add more sensors** - Temperature, humidity, light sensors
5. **Build a dashboard** - Web interface for monitoring and control

## 📚 Full Documentation

For detailed information, see the complete [README.md](README.md) which includes:
- Detailed hardware setup
- Advanced configuration options
- API integration guide
- Development and customization
- Troubleshooting guide

---

**Happy Plant Watering! 🌱💧**
