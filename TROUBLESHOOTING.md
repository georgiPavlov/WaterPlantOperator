# Troubleshooting Guide

Comprehensive troubleshooting guide for the WaterPlantOperator system.

## 🚨 Quick Diagnostics

### System Health Check
```bash
# Run comprehensive system check
python3 -c "
import sys
print('Python version:', sys.version)
try:
    import gpiozero
    print('✓ GPIO library available')
except ImportError:
    print('✗ GPIO library missing')

try:
    import picamera
    print('✓ Camera library available')
except ImportError:
    print('✗ Camera library missing')

try:
    import requests
    print('✓ HTTP library available')
except ImportError:
    print('✗ HTTP library missing')
"
```

### Hardware Test
```bash
# Test all hardware components
python3 -c "
from run.operation.pump import Pump
from run.sensor.moisture_sensor import Moisture
from gpiozero import LED
from picamera import PiCamera

print('Testing hardware components...')
try:
    pump = Pump(3000, 10, 100)
    print('✓ Pump initialized')
except Exception as e:
    print('✗ Pump error:', e)

try:
    sensor = Moisture(8)
    print('✓ Moisture sensor:', sensor.value)
except Exception as e:
    print('✗ Moisture sensor error:', e)

try:
    relay = LED(18)
    print('✓ Relay initialized')
except Exception as e:
    print('✗ Relay error:', e)

try:
    camera = PiCamera()
    print('✓ Camera initialized')
except Exception as e:
    print('✗ Camera error:', e)
"
```

## 🔧 Common Issues and Solutions

### 1. Permission Errors

#### Problem: "Permission denied" for GPIO
```
gpiozero.exc.BadPinFactory: Unable to load any default pin factory!
```

**Solutions:**
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo usermod -a -G spi $USER

# Reboot to apply changes
sudo reboot

# Verify group membership
groups $USER
```

#### Problem: "Permission denied" for camera
```
mmal: mmal_vc_component_create: failed to create component 'vc.ril.camera' (1:ENOMEM)
```

**Solutions:**
```bash
# Enable camera interface
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot after enabling
sudo reboot

# Test camera
libcamera-hello --list-cameras
```

### 2. Hardware Connection Issues

#### Problem: Moisture sensor always reads 0 or 1
**Symptoms:**
- Sensor value doesn't change
- Always returns 0.0 or 1.0
- No response to water/air

**Diagnosis:**
```bash
# Check GPIO pin status
gpio readall

# Test sensor directly
python3 -c "
from gpiozero import DigitalInputDevice
sensor = DigitalInputDevice(8)
print('Raw sensor value:', sensor.value)
"
```

**Solutions:**
1. **Check wiring:**
   ```
   Moisture Sensor → Raspberry Pi
   VCC → 5V (Pin 2)
   GND → GND (Pin 6)
   Signal → GPIO 8 (Pin 24)
   ```

2. **Test power supply:**
   ```bash
   # Check 5V power
   python3 -c "
   from gpiozero import LED
   led = LED(18)
   led.on()
   print('5V power test - LED should be on')
   "
   ```

3. **Replace sensor:**
   - Sensor may be damaged
   - Try different GPIO pin
   - Check for loose connections

#### Problem: Relay not switching pump
**Symptoms:**
- Pump doesn't turn on
- No clicking sound from relay
- LED on relay doesn't light up

**Diagnosis:**
```bash
# Test relay directly
python3 -c "
from gpiozero import LED
relay = LED(18)
print('Testing relay...')
relay.on()
print('Relay ON - should hear click')
import time
time.sleep(2)
relay.off()
print('Relay OFF')
"
```

**Solutions:**
1. **Check relay connections:**
   ```
   Relay Module → Raspberry Pi
   VCC → 5V (Pin 2)
   GND → GND (Pin 6)
   IN → GPIO 18 (Pin 12)
   ```

2. **Check pump power:**
   - Verify 12V power supply
   - Check pump connections
   - Test pump directly with 12V

3. **Check relay module:**
   - LED should light when activated
   - Listen for clicking sound
   - Test with multimeter

#### Problem: Camera not found
**Symptoms:**
```
picamera.exc.PiCameraError: Camera is not enabled
```

**Solutions:**
```bash
# Enable camera interface
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot system
sudo reboot

# Test camera
python3 -c "
from picamera import PiCamera
camera = PiCamera()
camera.capture('test.jpg')
print('Camera test successful')
"

# Alternative camera test
libcamera-hello --list-cameras
```

### 3. Software Issues

#### Problem: Module import errors
**Symptoms:**
```
ModuleNotFoundError: No module named 'run.operation.pump'
```

**Solutions:**
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Install missing dependencies
pip install -r requirements.txt

# Check virtual environment
which python3
source venv/bin/activate  # If using venv

# Verify project structure
ls -la run/
ls -la run/operation/
```

#### Problem: JSON parsing errors
**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**
```bash
# Test JSON functionality
python3 -c "
import json
from run.common.json_creator import get_json
result = get_json('{\"test\": \"value\"}')
print('JSON test:', result)
"

# Check server response
curl -X GET https://your-server.com/api/plan
```

#### Problem: Network connection issues
**Symptoms:**
```
requests.exceptions.ConnectionError: Failed to establish connection
```

**Solutions:**
```bash
# Test network connectivity
ping google.com
ping your-server.com

# Test DNS resolution
nslookup your-server.com

# Test API endpoint
curl -X GET https://your-server.com/api/plan

# Check firewall
sudo ufw status
```

### 4. Performance Issues

#### Problem: High CPU usage
**Symptoms:**
- System becomes slow
- High CPU usage in htop
- Delayed responses

**Diagnosis:**
```bash
# Check system resources
htop
free -h
df -h

# Check running processes
ps aux | grep python
```

**Solutions:**
```bash
# Optimize system
sudo apt update && sudo apt upgrade -y

# Clear unnecessary packages
sudo apt autoremove -y
sudo apt autoclean

# Check for background processes
sudo systemctl list-units --type=service --state=running
```

#### Problem: Memory leaks
**Symptoms:**
- Increasing memory usage over time
- System becomes unresponsive
- Out of memory errors

**Solutions:**
```bash
# Monitor memory usage
watch -n 1 'free -h'

# Check for memory leaks
python3 -c "
import psutil
import os
process = psutil.Process(os.getpid())
print('Memory usage:', process.memory_info().rss / 1024 / 1024, 'MB')
"

# Restart service if needed
sudo systemctl restart waterplant.service
```

### 5. Configuration Issues

#### Problem: Invalid configuration
**Symptoms:**
```
ValueError: Invalid configuration value
```

**Solutions:**
```bash
# Validate configuration
python3 -c "
from config.system_config import PUMP_CONFIG
print('Pump config:', PUMP_CONFIG)
"

# Check configuration file
cat config/system_config.py

# Reset to defaults
cp config/system_config.example.py config/system_config.py
```

#### Problem: Environment variables not loaded
**Symptoms:**
```
KeyError: 'SERVER_BASE_URL'
```

**Solutions:**
```bash
# Check environment variables
env | grep WATERPLANT

# Load environment file
source .env

# Set environment variables
export SERVER_BASE_URL=https://your-server.com/api
export API_KEY=your-api-key
```

## 🔍 Advanced Diagnostics

### System Logs Analysis

#### Check system logs
```bash
# View system logs
sudo journalctl -u waterplant.service -f

# View application logs
tail -f logs/waterplant.log

# Check boot logs
dmesg | tail -20

# Check kernel messages
sudo dmesg | grep -i error
```

#### Log analysis script
```python
# log_analyzer.py
import re
from datetime import datetime

def analyze_logs(log_file):
    errors = []
    warnings = []
    
    with open(log_file, 'r') as f:
        for line in f:
            if 'ERROR' in line:
                errors.append(line.strip())
            elif 'WARNING' in line:
                warnings.append(line.strip())
    
    print(f"Found {len(errors)} errors and {len(warnings)} warnings")
    
    if errors:
        print("\nRecent errors:")
        for error in errors[-5:]:  # Last 5 errors
            print(error)
    
    if warnings:
        print("\nRecent warnings:")
        for warning in warnings[-5:]:  # Last 5 warnings
            print(warning)

# Run analysis
analyze_logs('logs/waterplant.log')
```

### Hardware Diagnostics

#### GPIO diagnostics
```bash
# Check GPIO status
gpio readall

# Test individual pins
python3 -c "
from gpiozero import LED, Button
import time

# Test output pins
pins = [18, 21, 20, 16]
for pin in pins:
    try:
        led = LED(pin)
        led.on()
        print(f'GPIO {pin}: ON')
        time.sleep(0.5)
        led.off()
        print(f'GPIO {pin}: OFF')
    except Exception as e:
        print(f'GPIO {pin}: ERROR - {e}')
"

# Test input pins
python3 -c "
from gpiozero import Button
import time

pins = [8, 23, 24]
for pin in pins:
    try:
        button = Button(pin)
        print(f'GPIO {pin}: {button.value}')
    except Exception as e:
        print(f'GPIO {pin}: ERROR - {e}')
"
```

#### I2C diagnostics
```bash
# Check I2C devices
sudo i2cdetect -y 1

# Test I2C communication
python3 -c "
import smbus
bus = smbus.SMBus(1)
try:
    # Try to read from common I2C addresses
    for addr in range(0x48, 0x50):
        try:
            data = bus.read_byte(addr)
            print(f'I2C device found at address 0x{addr:02x}')
        except:
            pass
except Exception as e:
    print('I2C error:', e)
"
```

### Network Diagnostics

#### Network connectivity test
```bash
# Test network connectivity
ping -c 4 google.com
ping -c 4 your-server.com

# Test DNS resolution
nslookup your-server.com
dig your-server.com

# Test HTTP connectivity
curl -I https://your-server.com
curl -I https://your-server.com/api/plan

# Check network interfaces
ip addr show
ip route show
```

#### API connectivity test
```python
# api_test.py
import requests
import json

def test_api_connectivity():
    base_url = "https://your-server.com/api"
    api_key = "your-api-key"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test endpoints
    endpoints = [
        "/plan",
        "/water-level",
        "/picture"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
            print(f"{endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"{endpoint}: ERROR - {e}")

test_api_connectivity()
```

## 🛠️ Recovery Procedures

### System Recovery

#### Complete system reset
```bash
# Stop all services
sudo systemctl stop waterplant.service

# Backup configuration
cp config/system_config.py config/system_config.py.backup

# Reset to defaults
cp config/system_config.example.py config/system_config.py

# Clear logs
rm -f logs/*.log

# Restart service
sudo systemctl start waterplant.service
```

#### Hardware reset
```bash
# Reset GPIO pins
python3 -c "
from gpiozero import LED
import time

# Turn off all outputs
pins = [18, 21, 20, 16]
for pin in pins:
    try:
        led = LED(pin)
        led.off()
        print(f'GPIO {pin}: OFF')
    except:
        pass
"

# Reboot system
sudo reboot
```

### Data Recovery

#### Restore from backup
```bash
# Restore configuration
cp config/system_config.py.backup config/system_config.py

# Restore logs (if needed)
# Logs are typically not critical for operation

# Restore photos (if needed)
# Photos are stored in photos/ directory
```

## 📞 Getting Help

### Self-Help Resources

1. **Check logs first:**
   ```bash
   tail -f logs/waterplant.log
   sudo journalctl -u waterplant.service -f
   ```

2. **Run diagnostics:**
   ```bash
   python3 run_tests.py unit
   python3 run_tests.py integration
   ```

3. **Test hardware:**
   ```bash
   python3 -c "from run.operation.pump import Pump; print('Hardware test')"
   ```

### Community Support

1. **GitHub Issues:** Report bugs and feature requests
2. **Documentation:** Check README.md and other docs
3. **Forums:** Raspberry Pi forums for hardware issues

### Professional Support

For complex issues or production deployments:
- System administration support
- Hardware troubleshooting services
- Custom development services

## 📋 Maintenance Checklist

### Daily
- [ ] Check system status
- [ ] Verify water level
- [ ] Check moisture readings
- [ ] Review error logs

### Weekly
- [ ] Clean camera lens
- [ ] Check sensor connections
- [ ] Update system packages
- [ ] Backup configuration

### Monthly
- [ ] Clean water pump
- [ ] Check all wiring
- [ ] Update software
- [ ] Performance review

### Quarterly
- [ ] Replace sensors if needed
- [ ] Update hardware if required
- [ ] Security updates
- [ ] Full system backup

---

This troubleshooting guide should help you resolve most issues with the WaterPlantOperator system. For issues not covered here, please check the logs and consider opening a GitHub issue with detailed information about your setup and the problem you're experiencing.
