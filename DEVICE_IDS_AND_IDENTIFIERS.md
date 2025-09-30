# 🏷️ WaterPlantOperator Device IDs and Identifiers

## 📋 Overview

This document provides a comprehensive list of all device IDs, identifiers, and configuration values used in the WaterPlantOperator system.

---

## 🔑 Primary Device Identifiers

### **Main Device GUID**
```python
DEVICE_GUID = 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e'
```
- **Location**: `WaterPlantOperator/run/main.py:19`
- **Purpose**: Primary device identifier for server communication
- **Format**: UUID v4 format
- **Usage**: Used by `ServerCommunicator` for API authentication and device identification

### **Device ID Format**
The system uses various device ID formats depending on the context:

#### **Test Device IDs** (Used in testing)
- `TEST_DEVICE_001` - Primary test device
- `NEW_DEVICE_001` - New device creation tests
- `INTEGRATION_TEST_DEVICE` - Integration testing
- `HTTP_TEST_DEVICE_001` - HTTP API testing
- `DB_SYNC_DEVICE_001` - Database synchronization tests
- `CONSISTENCY_DEVICE_001` - Data consistency tests
- `PERF_DEVICE_001` to `PERF_DEVICE_999` - Performance testing
- `WORKFLOW_DEVICE_001` - Workflow testing
- `RECOVERY_DEVICE_001` - Recovery testing

#### **Production Device ID Examples**
- `raspberry-pi-001` - Example production device
- `test123` - Simple test device
- `设备_001` - Unicode device ID (Chinese characters)
- `SPECIAL_CHARS_001` - Special characters device ID

---

## 🔧 Hardware Configuration IDs

### **GPIO Pin Assignments**
```python
# From container_config.py
gpio_pins = {
    'pump': 18,              # Water pump control
    'valve': 19,             # Water valve control  
    'light': 20,             # Grow light control
    'moisture_sensor': 21,   # Moisture sensor input
    'water_level_sensor': 22 # Water level sensor input
}

# From main.py (original hardware)
MOISTURE_PIN = 4             # Moisture sensor pin
RELAY_PIN = 12               # Relay control pin
```

### **Sensor Configuration IDs**
```python
sensor_config = {
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
        'threshold': 25.0,   # Celsius
        'read_interval': 120 # seconds
    }
}
```

---

## 📁 File and Directory Identifiers

### **Photo Directory**
```python
PHOTO_DIR = '/tmp/device/photos'
```
- **Location**: `WaterPlantOperator/run/main.py:20`
- **Purpose**: Storage location for captured photos
- **Container Path**: `/app/data/` (mapped to host `./data/`)

### **Log Files**
- **Container Logs**: `/app/logs/`
- **Host Logs**: `./logs/`
- **Application Log**: `/tmp/example.log` (original)

---

## 🌐 Network and API Identifiers

### **API Endpoints**
- **Container API**: `http://localhost:8000`
- **Backend URL**: `http://host.docker.internal:8001`
- **API Key**: `your-api-key-here` (default)

### **Container Identifiers**
- **Container Name**: `waterplant-operator`
- **Image Name**: `localhost/waterplant-operator:latest`
- **Network**: `waterplant-network`

---

## ⚙️ System Configuration Identifiers

### **Watering Configuration**
```python
WATER_PUMPED_IN_SECOND = 70      # ml per second
WATER_MAX_CAPACITY = 2000        # ml
WATER_TIME_BETWEEN_CYCLE = 10    # seconds
MOISTURE_MAX_LEVEL = 0           # Maximum moisture level
DELAY_BETWEEN_PHOTO_TAKEN = 5    # seconds
```

### **Container Environment Variables**
```bash
ENVIRONMENT=container
SIMULATION_MODE=true
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
BACKEND_URL=http://host.docker.internal:8001
BACKEND_API_KEY=your-api-key-here
MOCK_GPIO=true
MOCK_CAMERA=true
MOCK_SENSORS=true
```

---

## 🏗️ Model and Database Identifiers

### **Device Model Fields**
```python
# Primary identifier
device_id = models.CharField(max_length=100, unique=True)

# Additional identifiers
label = models.CharField(max_length=200)
water_level = models.IntegerField()
moisture_level = models.IntegerField()
water_container_capacity = models.IntegerField()
is_connected = models.BooleanField()
```

### **Plan Model Identifiers**
```python
# Plan types
'basic'           # Basic watering plan
'moisture'        # Moisture-based plan
'time_based'      # Time-based plan
'delete'          # Plan deletion command
```

### **Status Model Identifiers**
```python
# Status types
'info'            # Information status
'warning'         # Warning status
'error'           # Error status
'success'         # Success status
```

---

## 📊 API Request/Response Identifiers

### **API Request Identifiers**
```json
{
  "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
  "label": "My Water Plant Device",
  "water_level": 75,
  "moisture_level": 45,
  "water_container_capacity": 2000,
  "is_connected": true
}
```

### **Plan Execution Identifiers**
```json
{
  "watering_status": true,
  "message": "[Plant successfully watered with moisture plan]",
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
  "plan_name": "smart_watering",
  "water_volume_used": 150
}
```

### **Sensor Data Identifiers**
```json
{
  "moisture_level": 45,
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e"
}
```

---

## 🔍 Device ID Usage Patterns

### **1. Server Communication**
The `DEVICE_GUID` is used in all server API calls:
- Health check reports
- Plan execution results
- Water level updates
- Moisture level reports
- Photo uploads

### **2. Database Operations**
Device IDs are used for:
- Device registration
- Plan association
- Status tracking
- Photo management
- Water chart data

### **3. API Endpoints**
Device IDs appear in URL paths:
```
/api/device/{device_id}/
/api/device/{device_id}/plans/
/api/device/{device_id}/status/
/api/device/{device_id}/photos/
```

### **4. Testing Scenarios**
Different device IDs are used for various test scenarios:
- **Unit Tests**: `TEST_DEVICE_001`
- **Integration Tests**: `INTEGRATION_TEST_DEVICE`
- **Performance Tests**: `PERF_DEVICE_001` to `PERF_DEVICE_999`
- **Error Tests**: `ERROR_DEVICE_001`

---

## 🛠️ Customization and Configuration

### **Changing Device GUID**
To change your device's primary identifier:

1. **Edit main.py**:
```python
DEVICE_GUID = 'your-new-device-guid-here'
```

2. **Update container environment**:
```bash
export DEVICE_GUID='your-new-device-guid-here'
```

3. **Rebuild container**:
```bash
./container_start.sh build
```

### **Adding New Device IDs**
For multiple devices, create additional configurations:

```python
# Multiple device configuration
DEVICES = {
    'device_1': {
        'guid': 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e',
        'label': 'Main Plant Device',
        'pins': {'pump': 18, 'valve': 19, 'light': 20}
    },
    'device_2': {
        'guid': 'cd424769-6e95-58e7-b4f2-c710d1ee2ff0',
        'label': 'Secondary Plant Device',
        'pins': {'pump': 21, 'valve': 22, 'light': 23}
    }
}
```

---

## 📋 Device ID Summary Table

| **Identifier Type** | **Value** | **Location** | **Purpose** |
|---------------------|-----------|--------------|-------------|
| **Primary Device GUID** | `ab313658-5d84-47d6-a3f1-b609c0f1dd5e` | `main.py:19` | Server communication |
| **Container Name** | `waterplant-operator` | `podman-compose.yml` | Container identification |
| **API Port** | `8000` | `container_config.py` | API endpoint |
| **Backend URL** | `http://host.docker.internal:8001` | `container_config.py` | Backend communication |
| **Photo Directory** | `/tmp/device/photos` | `main.py:20` | Photo storage |
| **Pump Pin** | `18` | `container_config.py` | Hardware control |
| **Valve Pin** | `19` | `container_config.py` | Hardware control |
| **Light Pin** | `20` | `container_config.py` | Hardware control |
| **Moisture Pin** | `21` | `container_config.py` | Sensor input |
| **Water Level Pin** | `22` | `container_config.py` | Sensor input |

---

## 🔧 Environment-Specific Identifiers

### **Development Environment**
- **Device GUID**: `ab313658-5d84-47d6-a3f1-b609c0f1dd5e`
- **API URL**: `http://localhost:8000`
- **Backend URL**: `http://localhost:8001`
- **Simulation Mode**: `true`

### **Production Environment**
- **Device GUID**: Should be unique per device
- **API URL**: `https://your-domain.com:8000`
- **Backend URL**: `https://your-backend.com:8001`
- **Simulation Mode**: `false`

### **Testing Environment**
- **Device GUID**: Various test IDs (`TEST_DEVICE_001`, etc.)
- **API URL**: `http://localhost:8000`
- **Backend URL**: `http://localhost:8001`
- **Simulation Mode**: `true`

---

## 🎯 Best Practices

### **Device ID Management**
1. **Use UUIDs** for primary device identification
2. **Keep device IDs unique** across all devices
3. **Use descriptive labels** for human-readable identification
4. **Version your device IDs** for tracking changes
5. **Document all custom identifiers** for team reference

### **Security Considerations**
1. **Don't expose device GUIDs** in public repositories
2. **Use environment variables** for sensitive identifiers
3. **Implement proper authentication** for device access
4. **Regularly rotate API keys** and device credentials
5. **Monitor device access** and usage patterns

---

## 📚 Related Documentation

- **API Documentation**: `API_DOCUMENTATION.md`
- **Container Setup**: `CONTAINER_README.md`
- **Integration Guide**: `COMPLETE_SYSTEM_INTEGRATION.md`
- **Test Results**: `CONTAINER_TEST_RESULTS.md`

---

**🏷️ Your WaterPlantOperator device is identified by GUID `ab313658-5d84-47d6-a3f1-b609c0f1dd5e` and can be customized for your specific needs! 🏷️**


