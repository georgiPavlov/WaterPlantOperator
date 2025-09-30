# 🌐 WaterPlantOperator API Documentation

## 📋 Overview

The WaterPlantOperator provides a comprehensive REST API for monitoring and controlling water plant automation systems. The API is designed to work both as a standalone containerized service and as part of the complete Water Plant Automation System.

## 🔗 Base URL

```
http://localhost:8000
```

## 🔐 Authentication

Currently, the containerized version does not require authentication. For production deployments, consider implementing API key authentication.

## 📊 API Categories

The WaterPlantOperator APIs are divided into two main categories:

1. **📈 Data Generation APIs** - Read-only endpoints that provide sensor data and system status
2. **🎛️ Control APIs** - Write endpoints that control hardware and generate actions

---

## 📈 Data Generation APIs

These APIs **generate and provide data** from sensors and system status.

### 1. Health & Status APIs

#### `GET /health`
**Purpose:** System health monitoring  
**Frequency:** On-demand or periodic health checks

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-29T16:27:19.380204",
  "environment": "container",
  "simulation_mode": true
}
```

**Example Usage:**
```bash
curl http://localhost:8000/health
```

---

#### `GET /status`
**Purpose:** Complete system status with sensor readings  
**Frequency:** On-demand or periodic status checks

**Response:**
```json
{
  "camera": {
    "available": true,
    "recording": false
  },
  "environment": "container",
  "relays": {
    "light": false,
    "pump": false,
    "valve": false
  },
  "sensors": {
    "humidity": 0.3282548556377715,
    "moisture": 0.8570205195884246,
    "temperature": 30.124016926502232,
    "water_level": 0.9148764335077473
  },
  "simulation_mode": true,
  "timestamp": "2025-09-29T16:27:24.031075"
}
```

**Example Usage:**
```bash
curl http://localhost:8000/status
```

---

#### `GET /config`
**Purpose:** Container configuration and settings  
**Frequency:** On-demand

**Response:**
```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "backend": {
    "url": "http://host.docker.internal:8001",
    "api_key": "your-api-key-here"
  },
  "camera": {
    "format": "jpeg",
    "quality": 85,
    "resolution": [1920, 1080]
  },
  "environment": "container",
  "gpio_pins": {
    "light": 20,
    "moisture_sensor": 21,
    "pump": 18,
    "valve": 19,
    "water_level_sensor": 22
  },
  "hardware": {
    "mock_camera": true,
    "mock_gpio": true,
    "mock_sensors": true
  },
  "log_level": "INFO",
  "pump": {
    "cooldown_time": 60,
    "flow_rate": 1.0,
    "max_runtime": 300,
    "pin": 18
  },
  "sensors": {
    "moisture": {
      "pin": 21,
      "read_interval": 30,
      "threshold": 0.3
    },
    "temperature": {
      "pin": 23,
      "read_interval": 120,
      "threshold": 25.0
    },
    "water_level": {
      "pin": 22,
      "read_interval": 60,
      "threshold": 0.2
    }
  },
  "simulation_mode": true,
  "watering": {
    "default_volume": 500,
    "max_daily_waterings": 5,
    "max_volume": 2000,
    "min_interval": 3600
  }
}
```

**Example Usage:**
```bash
curl http://localhost:8000/config
```

---

### 2. Sensor Data APIs

#### `GET /sensors`
**Purpose:** Current sensor readings  
**Frequency:** On-demand or periodic sensor monitoring

**Response:**
```json
{
  "humidity": 0.6509555693053541,
  "moisture": 0.8735460869463527,
  "temperature": 16.715594514013954,
  "water_level": 0.21438069543540667,
  "timestamp": "2025-09-29T16:27:29.021604"
}
```

**Sensor Data Types:**
- **moisture**: Soil moisture level (0.0-1.0, where 1.0 = 100% moisture)
- **temperature**: Ambient temperature in Celsius (15-35°C range)
- **humidity**: Air humidity level (0.0-1.0, where 1.0 = 100% humidity)
- **water_level**: Water tank level (0.0-1.0, where 1.0 = 100% full)

**Example Usage:**
```bash
curl http://localhost:8000/sensors
```

---

#### `GET /relays`
**Purpose:** Current relay states  
**Frequency:** On-demand or periodic hardware monitoring

**Response:**
```json
{
  "pump": false,
  "valve": false,
  "light": false
}
```

**Relay Types:**
- **pump**: Water pump control (true = on, false = off)
- **valve**: Water valve control (true = open, false = closed)
- **light**: Grow light control (true = on, false = off)

**Example Usage:**
```bash
curl http://localhost:8000/relays
```

---

## 🎛️ Control APIs

These APIs **control hardware and generate actions**.

### 1. Hardware Control APIs

#### `POST /relays`
**Purpose:** Control relay states  
**Frequency:** On-demand hardware control

**Request:**
```json
{
  "relay": "pump",
  "state": true
}
```

**Response:**
```json
{
  "relay": "pump",
  "state": true,
  "timestamp": "2025-09-29T16:27:34.091625"
}
```

**Parameters:**
- **relay**: Relay name (`pump`, `valve`, `light`)
- **state**: Boolean state (`true` = on, `false` = off)

**Example Usage:**
```bash
# Turn on pump
curl -X POST http://localhost:8000/relays \
  -H "Content-Type: application/json" \
  -d '{"relay": "pump", "state": true}'

# Turn off valve
curl -X POST http://localhost:8000/relays \
  -H "Content-Type: application/json" \
  -d '{"relay": "valve", "state": false}'
```

---

### 2. Camera Control APIs

#### `POST /camera/capture`
**Purpose:** Take a photo and generate image file  
**Frequency:** On-demand photo capture

**Request:**
```json
{
  "filename": "test_photo.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "test_photo.jpg",
  "path": "/app/data/test_photo.jpg",
  "timestamp": "2025-09-29T16:27:38.981656"
}
```

**Parameters:**
- **filename**: Optional filename (default: auto-generated with timestamp)

**Example Usage:**
```bash
# Take photo with custom filename
curl -X POST http://localhost:8000/camera/capture \
  -H "Content-Type: application/json" \
  -d '{"filename": "plant_photo_001.jpg"}'

# Take photo with auto-generated filename
curl -X POST http://localhost:8000/camera/capture \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 3. Watering Control APIs

#### `POST /watering/start`
**Purpose:** Start watering operation  
**Frequency:** On-demand watering control

**Request:**
```json
{
  "duration": 30
}
```

**Response:**
```json
{
  "success": true,
  "action": "watering_started",
  "duration": 30,
  "timestamp": "2025-09-29T16:27:48.284404"
}
```

**Parameters:**
- **duration**: Watering duration in seconds (default: 30)

**Example Usage:**
```bash
# Start watering for 30 seconds
curl -X POST http://localhost:8000/watering/start \
  -H "Content-Type: application/json" \
  -d '{"duration": 30}'

# Start watering with default duration
curl -X POST http://localhost:8000/watering/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

#### `POST /watering/stop`
**Purpose:** Stop watering operation  
**Frequency:** On-demand watering control

**Request:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "action": "watering_stopped",
  "timestamp": "2025-09-29T16:27:53.854917"
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:8000/watering/stop \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 📡 Original WaterPlantOperator Server Communication APIs

The original WaterPlantOperator communicates with a remote server using these additional APIs:

### Data Generation APIs (Operator → Server)

#### `POST /api/plan-execution`
**Purpose:** Report watering operation results  
**Frequency:** After each watering operation

**Request:**
```json
{
  "watering_status": true,
  "message": "[Plant successfully watered with moisture plan]",
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001",
  "plan_name": "smart_watering",
  "water_volume_used": 150
}
```

#### `POST /api/water`
**Purpose:** Report water tank level  
**Frequency:** After water level changes or every cycle

**Request:**
```json
{
  "water_level": 85.5,
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001"
}
```

#### `POST /api/moisture`
**Purpose:** Report soil moisture level  
**Frequency:** Every cycle or when moisture changes significantly

**Request:**
```json
{
  "moisture_level": 45,
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001"
}
```

#### `POST /api/picture`
**Purpose:** Upload captured plant photos  
**Frequency:** After photo capture

**Request:**
```http
POST /api/picture
Content-Type: multipart/form-data

{
  "photo": <image-file>,
  "filename": "plant_20231201_143022.jpg"
}
```

### Control APIs (Server → Operator)

#### `GET /api/plan`
**Purpose:** Retrieve watering instructions  
**Frequency:** Every cycle

**Response - No Plan:**
```json
{}
```

**Response - Basic Plan:**
```json
{
  "name": "daily_watering",
  "plan_type": "basic",
  "water_volume": 200
}
```

**Response - Moisture Plan:**
```json
{
  "name": "smart_watering",
  "plan_type": "moisture",
  "water_volume": 150,
  "moisture_threshold": 0.4,
  "check_interval": 30
}
```

**Response - Time Plan:**
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

#### `GET /api/picture`
**Purpose:** Check for photo capture requests  
**Frequency:** Every cycle

**Response - No Photo Request:**
```json
{}
```

**Response - Photo Request:**
```json
{
  "photo_id": "plant_photo_001",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

---

## 📊 Data Generation Summary

### Real-time Data Generation

The WaterPlantOperator continuously generates the following types of data:

#### 1. **Sensor Readings**
- **Moisture Levels**: Soil moisture measurements (0.0-1.0)
- **Temperature Readings**: Ambient temperature in Celsius (15-35°C)
- **Humidity Levels**: Air humidity measurements (0.0-1.0)
- **Water Level Readings**: Tank water level (0.0-1.0)

#### 2. **System Status**
- **Hardware States**: Relay states, camera availability
- **System Health**: Container status, simulation mode
- **Configuration**: Runtime settings and parameters

#### 3. **Operational Data**
- **Watering Operation Logs**: Start/stop events, duration, success/failure
- **Photo Capture Events**: Image files, timestamps, file paths
- **Error Logs**: System errors, hardware failures
- **Performance Metrics**: Response times, resource usage

### Control Operations

The WaterPlantOperator provides control over:

#### 1. **Hardware Control**
- **Relay Operations**: Pump, valve, and light control
- **Camera Operations**: Photo capture with custom filenames
- **Watering Operations**: Start/stop watering cycles with duration control

#### 2. **System Configuration**
- **Runtime Settings**: Configuration changes without restart
- **Hardware Simulation**: Mock hardware enable/disable
- **Logging Levels**: Dynamic log level adjustment

---

## 🔧 Integration Examples

### Python Integration

```python
import requests
import json

class WaterPlantOperator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_sensors(self):
        """Get current sensor readings"""
        response = requests.get(f"{self.base_url}/sensors")
        return response.json()
    
    def get_status(self):
        """Get system status"""
        response = requests.get(f"{self.base_url}/status")
        return response.json()
    
    def control_pump(self, state):
        """Control pump relay"""
        data = {"relay": "pump", "state": state}
        response = requests.post(
            f"{self.base_url}/relays",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        return response.json()
    
    def take_photo(self, filename=None):
        """Take a photo"""
        data = {"filename": filename} if filename else {}
        response = requests.post(
            f"{self.base_url}/camera/capture",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        return response.json()
    
    def start_watering(self, duration=30):
        """Start watering operation"""
        data = {"duration": duration}
        response = requests.post(
            f"{self.base_url}/watering/start",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        return response.json()
    
    def stop_watering(self):
        """Stop watering operation"""
        response = requests.post(
            f"{self.base_url}/watering/stop",
            headers={"Content-Type": "application/json"},
            data=json.dumps({})
        )
        return response.json()

# Usage example
operator = WaterPlantOperator()

# Get sensor data
sensors = operator.get_sensors()
print(f"Moisture: {sensors['moisture']:.2f}")
print(f"Temperature: {sensors['temperature']:.1f}°C")

# Control hardware
operator.control_pump(True)  # Turn on pump
operator.take_photo("plant_001.jpg")  # Take photo
operator.start_watering(60)  # Water for 60 seconds
```

### JavaScript/Node.js Integration

```javascript
const axios = require('axios');

class WaterPlantOperator {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async getSensors() {
        const response = await axios.get(`${this.baseUrl}/sensors`);
        return response.data;
    }
    
    async getStatus() {
        const response = await axios.get(`${this.baseUrl}/status`);
        return response.data;
    }
    
    async controlPump(state) {
        const response = await axios.post(`${this.baseUrl}/relays`, {
            relay: 'pump',
            state: state
        });
        return response.data;
    }
    
    async takePhoto(filename = null) {
        const data = filename ? { filename } : {};
        const response = await axios.post(`${this.baseUrl}/camera/capture`, data);
        return response.data;
    }
    
    async startWatering(duration = 30) {
        const response = await axios.post(`${this.baseUrl}/watering/start`, {
            duration: duration
        });
        return response.data;
    }
    
    async stopWatering() {
        const response = await axios.post(`${this.baseUrl}/watering/stop`, {});
        return response.data;
    }
}

// Usage example
const operator = new WaterPlantOperator();

async function monitorAndControl() {
    try {
        // Get sensor data
        const sensors = await operator.getSensors();
        console.log(`Moisture: ${sensors.moisture.toFixed(2)}`);
        console.log(`Temperature: ${sensors.temperature.toFixed(1)}°C`);
        
        // Control hardware based on conditions
        if (sensors.moisture < 0.3) {
            console.log('Moisture low, starting watering...');
            await operator.startWatering(45);
        }
        
        // Take photo
        const photo = await operator.takePhoto('monitoring_photo.jpg');
        console.log(`Photo saved: ${photo.filename}`);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

monitorAndControl();
```

---

## 🚨 Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Endpoint not found
- **500 Internal Server Error**: Server error

### Error Response Format

```json
{
  "error": "Error message description"
}
```

### Common Error Scenarios

1. **Invalid Relay Name**: `{"error": "Unknown relay: invalid_relay"}`
2. **Photo Capture Failure**: `{"error": "Failed to capture photo"}`
3. **Hardware Error**: `{"error": "Hardware operation failed"}`

---

## 📈 Monitoring and Logging

### Health Monitoring

The WaterPlantOperator provides comprehensive health monitoring:

- **Health Check Endpoint**: `/health` for basic health status
- **System Status**: `/status` for detailed system information
- **Configuration**: `/config` for runtime configuration

### Logging

All API operations are logged with:
- **Timestamp**: ISO format timestamps
- **Operation Type**: GET/POST operations
- **Parameters**: Request parameters and responses
- **Error Details**: Detailed error information

### Performance Metrics

- **Response Time**: <100ms for most operations
- **Throughput**: Handles multiple concurrent requests
- **Resource Usage**: Optimized for container environments

---

## 🔒 Security Considerations

### Current Implementation
- **No Authentication**: Containerized version runs without authentication
- **CORS Enabled**: Cross-origin requests allowed for development
- **Local Network**: Designed for local network deployment

### Production Recommendations
- **API Key Authentication**: Implement API key-based authentication
- **HTTPS**: Use HTTPS for production deployments
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Input Validation**: Validate all input parameters
- **Access Control**: Implement proper access control mechanisms

---

## 🎯 Use Cases

### 1. **Monitoring Dashboard**
- Real-time sensor data display
- System status monitoring
- Historical data visualization

### 2. **Automated Control**
- Moisture-based watering automation
- Scheduled watering operations
- Photo capture automation

### 3. **Integration with IoT Platforms**
- Data export to cloud platforms
- Integration with home automation systems
- Mobile app integration

### 4. **Research and Development**
- Plant growth monitoring
- Environmental data collection
- Automated experiment control

---

## 📚 Additional Resources

- **Container Setup**: See `CONTAINER_README.md`
- **Integration Guide**: See `COMPLETE_SYSTEM_INTEGRATION.md`
- **Test Results**: See `CONTAINER_TEST_RESULTS.md`
- **API Integration**: See `API_INTEGRATION.md`

---

**🌱 The WaterPlantOperator API provides a complete interface for monitoring and controlling water plant automation systems, making it perfect for integration with dashboards, mobile apps, and IoT platforms! 🌱**


