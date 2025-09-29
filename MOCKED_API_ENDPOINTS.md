# 🔌 Mocked API Endpoints - WaterPlantOperator Container

## 📋 Overview

The WaterPlantOperator container now includes **complete mocking** of all server communicator interface calls. This document lists all the mocked endpoints and their functionality.

---

## 🏷️ Device ID in Mock API

**Primary Device ID**: `ab313658-5d84-47d6-a3f1-b609c0f1dd5e`

This device ID is included in all API responses and is used for:
- Device identification
- Request routing
- Data association
- Logging and monitoring

---

## 🔌 Complete List of Mocked Endpoints

### **1. Health & Status Endpoints**

#### **GET /health**
- **Purpose**: Health check endpoint
- **Response**: System status with device ID
- **Example Response**:
```json
{
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "environment": "container",
    "simulation_mode": true,
    "status": "healthy",
    "timestamp": "2025-09-29T16:47:36.307624"
}
```

#### **GET /status**
- **Purpose**: Get system status with sensor readings
- **Response**: Complete system information including device ID
- **Example Response**:
```json
{
    "camera": {"available": true, "recording": false},
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "environment": "container",
    "relays": {"light": false, "pump": false, "valve": false},
    "sensors": {
        "humidity": 0.7178691043789689,
        "moisture": 0.5657075164491211,
        "temperature": 24.806881249406125,
        "water_level": 0.7502584110298431
    },
    "simulation_mode": true,
    "timestamp": "2025-09-29T16:43:22.139506"
}
```

#### **GET /sensors**
- **Purpose**: Get individual sensor readings
- **Response**: Sensor data with device ID
- **Example Response**:
```json
{
    "moisture": 0.5657075164491211,
    "temperature": 24.806881249406125,
    "humidity": 0.7178691043789689,
    "water_level": 0.7502584110298431,
    "timestamp": "2025-09-29T16:43:22.139506",
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e"
}
```

---

### **2. Server Communicator Interface Endpoints**

#### **GET /getPlan**
- **Purpose**: Mock getPlan endpoint - returns watering plans
- **Parameters**: `device` (query parameter)
- **Response**: Mock watering plan
- **Example Response**:
```json
{
    "name": "smart_watering",
    "plan_type": "moisture",
    "water_volume": 150,
    "moisture_threshold": 0.3,
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:47:41.533135"
}
```

#### **POST /postWater**
- **Purpose**: Mock postWater endpoint - receives water level updates
- **Request Body**: JSON with `device` and `water_level`
- **Response**: Confirmation with device ID
- **Example Request**:
```json
{
    "device": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "water_level": 75
}
```
- **Example Response**:
```json
{
    "success": true,
    "water_level": 75,
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:47:54.957594"
}
```

#### **POST /postMoisture**
- **Purpose**: Mock postMoisture endpoint - receives moisture level updates
- **Request Body**: JSON with `device` and `moisture_level`
- **Response**: Confirmation with device ID
- **Example Request**:
```json
{
    "device": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "moisture_level": 45
}
```
- **Example Response**:
```json
{
    "success": true,
    "moisture_level": 45,
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:47:59.367568"
}
```

#### **POST /postPhoto**
- **Purpose**: Mock postPhoto endpoint - receives photo uploads
- **Request**: Multipart form data with `image_file`, `device_id`, `photo_id`
- **Response**: Photo upload confirmation
- **Example Response**:
```json
{
    "success": true,
    "photo_id": "photo_001",
    "filename": "photo_001_20250929_164800.jpg",
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:48:00.000000"
}
```

#### **GET /getPhoto**
- **Purpose**: Mock getPhoto endpoint - returns photo capture requests
- **Parameters**: `device` (query parameter)
- **Response**: Photo capture request
- **Example Response**:
```json
{
    "action": "capture_photo",
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:48:13.582078"
}
```

#### **POST /postStatus**
- **Purpose**: Mock postStatus endpoint - receives plan execution status
- **Request Body**: JSON with `device`, `execution_status`, `message`
- **Response**: Status confirmation
- **Example Request**:
```json
{
    "device": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "execution_status": true,
    "message": "Plant successfully watered"
}
```
- **Example Response**:
```json
{
    "success": true,
    "execution_status": true,
    "message": "Plant successfully watered",
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:48:04.732563"
}
```

#### **GET /getWaterLevel**
- **Purpose**: Mock getWaterLevel endpoint - returns water level reset requests
- **Parameters**: `device` (query parameter)
- **Response**: Water level reset request
- **Example Response**:
```json
{
    "action": "reset_water_level",
    "device_id": "ab313658-5d84-47d6-a3f1-b609c0f1dd5e",
    "timestamp": "2025-09-29T16:48:08.628477"
}
```

---

### **3. Hardware Control Endpoints**

#### **GET/POST /relays**
- **Purpose**: Control relay states (pump, valve, light)
- **GET Response**: Current relay states
- **POST Request**: JSON with `relay` and `state`
- **Example GET Response**:
```json
{
    "light": false,
    "pump": false,
    "valve": false
}
```

#### **POST /camera/capture**
- **Purpose**: Take a photo
- **Request Body**: JSON with optional `filename`
- **Response**: Photo capture confirmation

#### **POST /watering/start**
- **Purpose**: Start watering operation
- **Request Body**: JSON with optional `duration`
- **Response**: Watering start confirmation

#### **POST /watering/stop**
- **Purpose**: Stop watering operation
- **Response**: Watering stop confirmation

#### **GET /config**
- **Purpose**: Get container configuration
- **Response**: Complete configuration dictionary

---

## 🔄 Server Communicator Interface Mapping

| **Original Method** | **Mock Endpoint** | **HTTP Method** | **Purpose** |
|---------------------|-------------------|-----------------|-------------|
| `get_plan()` | `/getPlan` | GET | Get watering plans |
| `post_water()` | `/postWater` | POST | Send water level updates |
| `post_moisture()` | `/postMoisture` | POST | Send moisture level updates |
| `post_picture()` | `/postPhoto` | POST | Upload photos |
| `get_picture()` | `/getPhoto` | GET | Get photo capture requests |
| `post_plan_execution()` | `/postStatus` | POST | Send execution status |
| `get_water_level()` | `/getWaterLevel` | GET | Get water level reset requests |

---

## 🧪 Testing the Mocked Endpoints

### **Test Commands**

```bash
# Health check
curl -s http://localhost:8000/health | python3 -m json.tool

# Get plan
curl -s "http://localhost:8000/getPlan?device=ab313658-5d84-47d6-a3f1-b609c0f1dd5e" | python3 -m json.tool

# Post water level
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"device":"ab313658-5d84-47d6-a3f1-b609c0f1dd5e","water_level":75}' \
  http://localhost:8000/postWater | python3 -m json.tool

# Post moisture level
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"device":"ab313658-5d84-47d6-a3f1-b609c0f1dd5e","moisture_level":45}' \
  http://localhost:8000/postMoisture | python3 -m json.tool

# Post status
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"device":"ab313658-5d84-47d6-a3f1-b609c0f1dd5e","execution_status":true,"message":"Plant successfully watered"}' \
  http://localhost:8000/postStatus | python3 -m json.tool

# Get water level
curl -s "http://localhost:8000/getWaterLevel?device=ab313658-5d84-47d6-a3f1-b609c0f1dd5e" | python3 -m json.tool

# Get photo request
curl -s "http://localhost:8000/getPhoto?device=ab313658-5d84-47d6-a3f1-b609c0f1dd5e" | python3 -m json.tool
```

---

## ✅ Complete Mocking Status

**All server communicator interface calls are now fully mocked:**

- ✅ **get_plan()** → `/getPlan`
- ✅ **post_water()** → `/postWater`
- ✅ **post_moisture()** → `/postMoisture`
- ✅ **post_picture()** → `/postPhoto`
- ✅ **get_picture()** → `/getPhoto`
- ✅ **post_plan_execution()** → `/postStatus`
- ✅ **get_water_level()** → `/getWaterLevel`

**Additional endpoints:**
- ✅ **Health check** → `/health`
- ✅ **System status** → `/status`
- ✅ **Sensor readings** → `/sensors`
- ✅ **Relay control** → `/relays`
- ✅ **Camera capture** → `/camera/capture`
- ✅ **Watering control** → `/watering/start`, `/watering/stop`
- ✅ **Configuration** → `/config`

---

## 🎯 Device ID Usage

The device ID `ab313658-5d84-47d6-a3f1-b609c0f1dd5e` is:

1. **Included in all responses** for device identification
2. **Used for request routing** and data association
3. **Logged in all operations** for tracking and debugging
4. **Consistent across all endpoints** for unified device management
5. **Available in both query parameters and request bodies** for flexibility

---

**🔌 All server communicator interface calls are now fully mocked and functional in the WaterPlantOperator container! 🔌**
