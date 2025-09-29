# Hardware Setup Guide

Complete guide for setting up the WaterPlantOperator hardware on Raspberry Pi.

## 📋 Required Components

### Essential Components

| Component | Quantity | Purpose | Price Range |
|-----------|----------|---------|-------------|
| **Raspberry Pi 4** (4GB+) | 1 | Main controller | $55-75 |
| **MicroSD Card** (32GB+) | 1 | Operating system storage | $10-20 |
| **Capacitive Moisture Sensor** | 1-3 | Soil moisture detection | $5-15 |
| **12V Water Pump** | 1 | Water delivery | $10-25 |
| **Relay Module** (5V) | 1 | Pump control | $3-8 |
| **Raspberry Pi Camera** | 1 | Plant photography | $25-35 |
| **Power Supply 5V/3A** | 1 | Pi power | $8-15 |
| **Power Supply 12V/2A** | 1 | Pump power | $10-20 |
| **Jumper Wires** | 1 set | Connections | $5-10 |
| **Breadboard** | 1 | Prototyping | $5-10 |

### Optional Components

| Component | Quantity | Purpose | Price Range |
|-----------|----------|---------|-------------|
| **Water Level Sensor** | 1 | Tank monitoring | $8-15 |
| **LED Indicators** | 3-5 | Status display | $2-5 |
| **Buzzer** | 1 | Audio alerts | $2-5 |
| **LCD Display** (16x2) | 1 | Local status | $8-15 |
| **Push Buttons** | 2-3 | Manual control | $2-5 |
| **Resistors** (220Ω, 10kΩ) | 1 set | Circuit protection | $3-8 |
| **Waterproof Enclosure** | 1 | Outdoor protection | $15-30 |

**Total Cost: $150-300** (depending on components and quality)

## 🔌 Wiring Diagrams

### Basic Setup (Essential Components)

```
                    Raspberry Pi 4
                    ┌─────────────┐
                    │             │
                    │  GPIO 18 ───┼─── Relay IN
                    │  GPIO 8  ───┼─── Moisture Sensor Signal
                    │  5V      ───┼─── Moisture Sensor VCC
                    │  GND     ───┼─── Moisture Sensor GND
                    │             │
                    │  Camera Port ─── Pi Camera
                    │             │
                    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    │  12V Supply ─── Water Pump
                    │             │
                    └─────────────┘
```

### Detailed Pin Connections

#### Raspberry Pi 4 GPIO Layout
```
     3V3  (1) (2)  5V
   GPIO2  (3) (4)  5V
   GPIO3  (5) (6)  GND
   GPIO4  (7) (8)  GPIO14
     GND  (9) (10) GPIO15
  GPIO17 (11) (12) GPIO18  ← Relay Control
  GPIO27 (13) (14) GND
  GPIO22 (15) (16) GPIO23
     3V3 (17) (18) GPIO24
  GPIO10 (19) (20) GND
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8   ← Moisture Sensor
     GND (25) (26) GPIO7
```

#### Component Connections

**Relay Module:**
```
Relay Module    →    Raspberry Pi
VCC            →    5V (Pin 2)
GND            →    GND (Pin 6)
IN             →    GPIO 18 (Pin 12)
```

**Moisture Sensor:**
```
Moisture Sensor →    Raspberry Pi
VCC            →    5V (Pin 2)
GND            →    GND (Pin 6)
Signal         →    GPIO 8 (Pin 24)
```

**Water Pump:**
```
Water Pump     →    Relay Module
Positive       →    NO (Normally Open)
Negative       →    12V Power Supply Negative
12V Supply     →    Relay Module COM
```

### Advanced Setup (With Optional Components)

```
                    Raspberry Pi 4
                    ┌─────────────┐
                    │             │
                    │  GPIO 18 ───┼─── Relay IN
                    │  GPIO 8  ───┼─── Moisture Sensor Signal
                    │  GPIO 2  ───┼─── Water Level Sensor (I2C SDA)
                    │  GPIO 3  ───┼─── Water Level Sensor (I2C SCL)
                    │  GPIO 21 ───┼─── Status LED
                    │  GPIO 20 ───┼─── Error LED
                    │  GPIO 16 ───┼─── Buzzer
                    │  GPIO 23 ───┼─── Manual Water Button
                    │  GPIO 24 ───┼─── Emergency Stop Button
                    │  5V      ───┼─── Sensor Power
                    │  GND     ───┼─── Common Ground
                    │             │
                    │  Camera Port ─── Pi Camera
                    │             │
                    └─────────────┘
```

## 🛠️ Step-by-Step Assembly

### Step 1: Prepare the Raspberry Pi

1. **Flash the OS:**
   ```bash
   # Download Raspberry Pi Imager
   # Flash Raspberry Pi OS (64-bit) to SD card
   # Enable SSH and configure WiFi during setup
   ```

2. **Enable Interfaces:**
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   # Interface Options → I2C → Enable
   # Interface Options → SPI → Enable
   # Interface Options → SSH → Enable
   ```

3. **Update System:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-pip python3-venv git
   ```

### Step 2: Connect Basic Components

#### Relay Module Connection
```
1. Connect relay VCC to Pi 5V (Pin 2)
2. Connect relay GND to Pi GND (Pin 6)
3. Connect relay IN to Pi GPIO 18 (Pin 12)
4. Connect 12V power supply positive to relay COM
5. Connect water pump positive to relay NO
6. Connect water pump negative to 12V power supply negative
```

#### Moisture Sensor Connection
```
1. Connect sensor VCC to Pi 5V (Pin 2)
2. Connect sensor GND to Pi GND (Pin 6)
3. Connect sensor Signal to Pi GPIO 8 (Pin 24)
```

#### Camera Connection
```
1. Insert camera ribbon cable into camera port
2. Secure camera in desired position
3. Test camera: python3 -c "from picamera import PiCamera; PiCamera().capture('test.jpg')"
```

### Step 3: Add Optional Components

#### Water Level Sensor (I2C)
```
1. Connect sensor VCC to Pi 5V (Pin 2)
2. Connect sensor GND to Pi GND (Pin 6)
3. Connect sensor SDA to Pi GPIO 2 (Pin 3)
4. Connect sensor SCL to Pi GPIO 3 (Pin 5)
```

#### Status LEDs
```
1. Connect LED anode to Pi GPIO 21 (Pin 40) via 220Ω resistor
2. Connect LED cathode to Pi GND (Pin 6)
3. Repeat for error LED on GPIO 20 (Pin 38)
```

#### Buzzer
```
1. Connect buzzer positive to Pi GPIO 16 (Pin 36)
2. Connect buzzer negative to Pi GND (Pin 6)
```

#### Manual Control Buttons
```
1. Connect button one side to Pi GPIO 23 (Pin 16)
2. Connect button other side to Pi GND (Pin 6)
3. Add 10kΩ pull-up resistor between GPIO and 3.3V
4. Repeat for emergency stop button on GPIO 24 (Pin 18)
```

### Step 4: Power Supply Setup

#### Raspberry Pi Power
```
1. Use official 5V/3A power supply
2. Connect to Pi power port
3. Ensure stable power for reliable operation
```

#### Water Pump Power
```
1. Use 12V/2A power supply for pump
2. Connect positive to relay COM terminal
3. Connect negative to pump negative terminal
4. Use appropriate gauge wire for current capacity
```

## 🧪 Hardware Testing

### Test Scripts

Create test files to verify each component:

#### 1. GPIO Test
```python
# test_gpio.py
from gpiozero import LED, Button
import time

def test_relay():
    relay = LED(18)
    print("Testing relay...")
    relay.on()
    print("Relay ON - pump should be running")
    time.sleep(2)
    relay.off()
    print("Relay OFF - pump should stop")

def test_leds():
    status_led = LED(21)
    error_led = LED(20)
    print("Testing LEDs...")
    status_led.on()
    time.sleep(1)
    status_led.off()
    error_led.on()
    time.sleep(1)
    error_led.off()

def test_buzzer():
    buzzer = LED(16)
    print("Testing buzzer...")
    buzzer.on()
    time.sleep(0.5)
    buzzer.off()

if __name__ == "__main__":
    test_relay()
    test_leds()
    test_buzzer()
    print("GPIO tests completed")
```

#### 2. Sensor Test
```python
# test_sensors.py
from run.sensor.moisture_sensor import Moisture
import time

def test_moisture_sensor():
    sensor = Moisture(8)
    print("Testing moisture sensor...")
    for i in range(5):
        value = sensor.value
        print(f"Moisture reading {i+1}: {value:.3f}")
        time.sleep(1)

if __name__ == "__main__":
    test_moisture_sensor()
```

#### 3. Camera Test
```python
# test_camera.py
from picamera import PiCamera
import time

def test_camera():
    camera = PiCamera()
    print("Testing camera...")
    camera.start_preview()
    time.sleep(2)
    camera.capture('test_image.jpg')
    camera.stop_preview()
    print("Photo captured: test_image.jpg")

if __name__ == "__main__":
    test_camera()
```

### Running Tests

```bash
# Test individual components
python3 test_gpio.py
python3 test_sensors.py
python3 test_camera.py

# Test complete system
python3 -c "
from run.operation.pump import Pump
from run.sensor.moisture_sensor import Moisture
pump = Pump(3000, 10, 100)
sensor = Moisture(8)
print('System test: OK')
"
```

## 🔧 Troubleshooting

### Common Hardware Issues

#### 1. Relay Not Working
**Symptoms:** Pump doesn't turn on
**Solutions:**
- Check relay power supply (5V)
- Verify GPIO 18 connection
- Test relay with multimeter
- Check pump power supply (12V)

#### 2. Moisture Sensor Reading 0
**Symptoms:** Sensor always reads 0 or 1
**Solutions:**
- Check sensor power (5V and GND)
- Verify GPIO 8 connection
- Test sensor in water vs air
- Check sensor for damage

#### 3. Camera Not Found
**Symptoms:** "Camera not found" error
**Solutions:**
- Enable camera in raspi-config
- Check ribbon cable connection
- Reboot after enabling camera
- Test with: `libcamera-hello --list-cameras`

#### 4. GPIO Permission Errors
**Symptoms:** "Permission denied" for GPIO
**Solutions:**
```bash
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo reboot
```

#### 5. Power Issues
**Symptoms:** System reboots or unstable
**Solutions:**
- Use official Pi power supply
- Check power supply capacity
- Use shorter, thicker power cables
- Add capacitors for power smoothing

### Diagnostic Commands

```bash
# Check GPIO status
gpio readall

# Check I2C devices
sudo i2cdetect -y 1

# Check camera
libcamera-hello --list-cameras

# Check system resources
htop
df -h
free -h

# Check system logs
sudo journalctl -f
dmesg | tail
```

## 🏠 Enclosure and Protection

### Indoor Setup
- Use plastic project box
- Add ventilation holes
- Mount on wall or shelf
- Protect from water splashes

### Outdoor Setup
- Use waterproof enclosure (IP65+)
- Add desiccant for moisture control
- Use UV-resistant materials
- Ground all metal components

### Cable Management
- Use cable ties and conduits
- Label all connections
- Protect cables from weather
- Use appropriate gauge wire

## 📊 Performance Optimization

### Power Management
- Use efficient power supplies
- Implement sleep modes for sensors
- Monitor power consumption
- Add backup power if needed

### Signal Quality
- Use short, shielded cables
- Add pull-up/pull-down resistors
- Filter power supply noise
- Ground all components properly

### Environmental Protection
- Seal all connections
- Use weatherproof connectors
- Add surge protection
- Monitor temperature and humidity

---

## 🎯 Next Steps

After hardware setup is complete:

1. **Install Software** - Follow the software installation guide
2. **Configure System** - Set up configuration files
3. **Test Integration** - Run full system tests
4. **Deploy** - Set up as a service for automatic startup
5. **Monitor** - Set up logging and monitoring

For software setup, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md).
