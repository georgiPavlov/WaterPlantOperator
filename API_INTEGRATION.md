# API Integration Guide

Complete guide for integrating the WaterPlantOperator with your server and building a monitoring dashboard.

## 🌐 API Overview

The WaterPlantOperator communicates with a remote server using REST API endpoints. This allows for:
- Remote monitoring and control
- Data collection and analytics
- Automated notifications
- Multi-device management

## 📡 API Endpoints

### Base URL
```
https://your-server.com/api
```

### Authentication
All API requests require authentication using an API key:
```http
Authorization: Bearer your-api-key-here
```

## 🔄 Core API Endpoints

### 1. Health Check
**Endpoint:** `POST /api/plan-execution`  
**Purpose:** System health monitoring  
**Frequency:** Every cycle (default: 60 seconds)

```http
POST /api/plan-execution
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "watering_status": false,
  "message": "healthcheck",
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001"
}
```

**Response:**
```json
{
  "status": "received",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

### 2. Get Watering Plan
**Endpoint:** `GET /api/plan`  
**Purpose:** Retrieve watering instructions  
**Frequency:** Every cycle

```http
GET /api/plan
Authorization: Bearer your-api-key
```

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

**Response - Delete Plan:**
```json
{
  "plan_type": "delete"
}
```

### 3. Post Execution Results
**Endpoint:** `POST /api/plan-execution`  
**Purpose:** Report watering operation results  
**Frequency:** After each watering operation

```http
POST /api/plan-execution
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "watering_status": true,
  "message": "[Plant successfully watered with moisture plan]",
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001",
  "plan_name": "smart_watering",
  "water_volume_used": 150
}
```

**Response:**
```json
{
  "status": "received",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

### 4. Post Water Level
**Endpoint:** `POST /api/water`  
**Purpose:** Report current water tank level  
**Frequency:** After water level changes or every cycle

```http
POST /api/water
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "water_level": 85.5,
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001"
}
```

**Response:**
```json
{
  "status": "received",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

### 5. Post Moisture Level
**Endpoint:** `POST /api/moisture`  
**Purpose:** Report current soil moisture level  
**Frequency:** Every cycle or when moisture changes significantly

```http
POST /api/moisture
Content-Type: application/json
Authorization: Bearer your-api-key

{
  "moisture_level": 45,
  "timestamp": "2023-12-01T14:30:22Z",
  "device_id": "raspberry-pi-001"
}
```

**Response:**
```json
{
  "status": "received",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

### 6. Get Photo Request
**Endpoint:** `GET /api/picture`  
**Purpose:** Check for photo capture requests  
**Frequency:** Every cycle

```http
GET /api/picture
Authorization: Bearer your-api-key
```

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

### 7. Post Photo
**Endpoint:** `POST /api/picture`  
**Purpose:** Upload captured plant photos  
**Frequency:** When photo is requested and captured

```http
POST /api/picture
Content-Type: multipart/form-data
Authorization: Bearer your-api-key

photo: <binary-image-data>
filename: "plant_20231201_143022.jpg"
photo_id: "plant_photo_001"
timestamp: "2023-12-01T14:30:22Z"
device_id: "raspberry-pi-001"
```

**Response:**
```json
{
  "status": "received",
  "photo_url": "https://your-server.com/photos/plant_20231201_143022.jpg",
  "timestamp": "2023-12-01T14:30:22Z"
}
```

### 8. Get Water Level Update
**Endpoint:** `GET /api/water-level`  
**Purpose:** Check for water level updates from server  
**Frequency:** Every cycle

```http
GET /api/water-level
Authorization: Bearer your-api-key
```

**Response - No Update:**
```json
{}
```

**Response - Water Level Update:**
```json
{
  "water": 3000,
  "timestamp": "2023-12-01T14:30:22Z"
}
```

## 🖥️ Server Implementation Examples

### Flask Server (Python)

```python
from flask import Flask, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage (use database in production)
plans = {}
photos = {}
water_levels = {}
moisture_levels = {}

@app.route('/api/plan', methods=['GET'])
def get_plan():
    """Get watering plan for device"""
    device_id = request.headers.get('X-Device-ID', 'default')
    
    # Return plan if exists, otherwise empty JSON
    plan = plans.get(device_id)
    if plan:
        # Remove plan after sending (one-time execution)
        del plans[device_id]
        return jsonify(plan)
    
    return jsonify({})

@app.route('/api/plan-execution', methods=['POST'])
def post_plan_execution():
    """Receive watering execution results"""
    data = request.json
    device_id = data.get('device_id', 'unknown')
    
    # Log execution result
    print(f"Device {device_id}: {data['message']}")
    
    # Store result for dashboard
    # In production, save to database
    
    return jsonify({
        "status": "received",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/water', methods=['POST'])
def post_water():
    """Receive water level updates"""
    data = request.json
    device_id = data.get('device_id', 'unknown')
    
    # Store water level
    water_levels[device_id] = {
        "level": data['water_level'],
        "timestamp": data['timestamp']
    }
    
    return jsonify({"status": "received"})

@app.route('/api/moisture', methods=['POST'])
def post_moisture():
    """Receive moisture level updates"""
    data = request.json
    device_id = data.get('device_id', 'unknown')
    
    # Store moisture level
    moisture_levels[device_id] = {
        "level": data['moisture_level'],
        "timestamp": data['timestamp']
    }
    
    return jsonify({"status": "received"})

@app.route('/api/picture', methods=['GET'])
def get_picture_request():
    """Check for photo requests"""
    device_id = request.headers.get('X-Device-ID', 'default')
    
    # Return photo request if exists
    photo_request = photos.get(device_id)
    if photo_request:
        del photos[device_id]  # Remove after sending
        return jsonify(photo_request)
    
    return jsonify({})

@app.route('/api/picture', methods=['POST'])
def post_picture():
    """Receive uploaded photos"""
    if 'photo' not in request.files:
        return jsonify({"error": "No photo provided"}), 400
    
    photo = request.files['photo']
    filename = request.form.get('filename', 'unknown.jpg')
    
    # Save photo
    photo.save(f"uploads/{filename}")
    
    return jsonify({
        "status": "received",
        "photo_url": f"/uploads/{filename}"
    })

@app.route('/api/water-level', methods=['GET'])
def get_water_level():
    """Get water level updates"""
    device_id = request.headers.get('X-Device-ID', 'default')
    
    # Return water level update if exists
    water_update = water_levels.get(f"{device_id}_update")
    if water_update:
        del water_levels[f"{device_id}_update"]
        return jsonify(water_update)
    
    return jsonify({})

# Dashboard endpoints
@app.route('/api/dashboard/status')
def dashboard_status():
    """Get dashboard data"""
    return jsonify({
        "devices": list(water_levels.keys()),
        "water_levels": water_levels,
        "moisture_levels": moisture_levels
    })

@app.route('/api/dashboard/send-plan', methods=['POST'])
def send_plan():
    """Send plan to device"""
    data = request.json
    device_id = data['device_id']
    plan = data['plan']
    
    plans[device_id] = plan
    return jsonify({"status": "plan_sent"})

@app.route('/api/dashboard/request-photo', methods=['POST'])
def request_photo():
    """Request photo from device"""
    data = request.json
    device_id = data['device_id']
    photo_id = data['photo_id']
    
    photos[device_id] = {
        "photo_id": photo_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return jsonify({"status": "photo_requested"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Node.js Server (Express)

```javascript
const express = require('express');
const multer = require('multer');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('uploads'));

// Storage
const plans = new Map();
const photos = new Map();
const waterLevels = new Map();
const moistureLevels = new Map();

// Multer configuration for file uploads
const upload = multer({ dest: 'uploads/' });

// API Routes
app.get('/api/plan', (req, res) => {
    const deviceId = req.headers['x-device-id'] || 'default';
    const plan = plans.get(deviceId);
    
    if (plan) {
        plans.delete(deviceId); // One-time execution
        res.json(plan);
    } else {
        res.json({});
    }
});

app.post('/api/plan-execution', (req, res) => {
    const data = req.body;
    const deviceId = data.device_id || 'unknown';
    
    console.log(`Device ${deviceId}: ${data.message}`);
    
    res.json({
        status: 'received',
        timestamp: new Date().toISOString()
    });
});

app.post('/api/water', (req, res) => {
    const data = req.body;
    const deviceId = data.device_id || 'unknown';
    
    waterLevels.set(deviceId, {
        level: data.water_level,
        timestamp: data.timestamp
    });
    
    res.json({ status: 'received' });
});

app.post('/api/moisture', (req, res) => {
    const data = req.body;
    const deviceId = data.device_id || 'unknown';
    
    moistureLevels.set(deviceId, {
        level: data.moisture_level,
        timestamp: data.timestamp
    });
    
    res.json({ status: 'received' });
});

app.get('/api/picture', (req, res) => {
    const deviceId = req.headers['x-device-id'] || 'default';
    const photoRequest = photos.get(deviceId);
    
    if (photoRequest) {
        photos.delete(deviceId);
        res.json(photoRequest);
    } else {
        res.json({});
    }
});

app.post('/api/picture', upload.single('photo'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No photo provided' });
    }
    
    const filename = req.body.filename || req.file.originalname;
    
    res.json({
        status: 'received',
        photo_url: `/uploads/${filename}`
    });
});

// Dashboard endpoints
app.get('/api/dashboard/status', (req, res) => {
    res.json({
        devices: Array.from(waterLevels.keys()),
        waterLevels: Object.fromEntries(waterLevels),
        moistureLevels: Object.fromEntries(moistureLevels)
    });
});

app.post('/api/dashboard/send-plan', (req, res) => {
    const { device_id, plan } = req.body;
    plans.set(device_id, plan);
    res.json({ status: 'plan_sent' });
});

app.post('/api/dashboard/request-photo', (req, res) => {
    const { device_id, photo_id } = req.body;
    photos.set(device_id, {
        photo_id,
        timestamp: new Date().toISOString()
    });
    res.json({ status: 'photo_requested' });
});

app.listen(5000, () => {
    console.log('Server running on port 5000');
});
```

## 📊 Dashboard Implementation

### Simple HTML Dashboard

```html
<!DOCTYPE html>
<html>
<head>
    <title>WaterPlantOperator Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 10px 0; }
        .status { display: flex; justify-content: space-between; align-items: center; }
        .metric { text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; }
        .metric-label { color: #666; }
        .button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .button:hover { background: #0056b3; }
        .form-group { margin: 10px 0; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>WaterPlantOperator Dashboard</h1>
        
        <!-- Device Status -->
        <div class="card">
            <h2>Device Status</h2>
            <div id="device-status">Loading...</div>
        </div>
        
        <!-- Current Metrics -->
        <div class="card">
            <h2>Current Metrics</h2>
            <div class="status">
                <div class="metric">
                    <div class="metric-value" id="water-level">--</div>
                    <div class="metric-label">Water Level (%)</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="moisture-level">--</div>
                    <div class="metric-label">Moisture Level (%)</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="last-watering">--</div>
                    <div class="metric-label">Last Watering</div>
                </div>
            </div>
        </div>
        
        <!-- Send Plan -->
        <div class="card">
            <h2>Send Watering Plan</h2>
            <form id="plan-form">
                <div class="form-group">
                    <label>Plan Type:</label>
                    <select id="plan-type">
                        <option value="basic">Basic</option>
                        <option value="moisture">Moisture-based</option>
                        <option value="time_based">Time-based</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Water Volume (ml):</label>
                    <input type="number" id="water-volume" value="200" min="50" max="1000">
                </div>
                <div class="form-group" id="moisture-options" style="display: none;">
                    <label>Moisture Threshold (0.0-1.0):</label>
                    <input type="number" id="moisture-threshold" value="0.4" min="0.1" max="1.0" step="0.1">
                </div>
                <div class="form-group" id="time-options" style="display: none;">
                    <label>Watering Times (comma-separated):</label>
                    <input type="text" id="watering-times" placeholder="08:00,18:00">
                </div>
                <button type="submit" class="button">Send Plan</button>
            </form>
        </div>
        
        <!-- Photo Management -->
        <div class="card">
            <h2>Photo Management</h2>
            <button onclick="requestPhoto()" class="button">Request Photo</button>
            <div id="photo-container"></div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000/api';
        let currentDevice = 'raspberry-pi-001';
        
        // Update dashboard data
        async function updateDashboard() {
            try {
                const response = await fetch(`${API_BASE}/dashboard/status`);
                const data = await response.json();
                
                // Update device status
                document.getElementById('device-status').innerHTML = 
                    `Connected devices: ${data.devices.length}`;
                
                // Update metrics for first device
                if (data.devices.length > 0) {
                    const device = data.devices[0];
                    const waterLevel = data.waterLevels[device];
                    const moistureLevel = data.moistureLevels[device];
                    
                    if (waterLevel) {
                        document.getElementById('water-level').textContent = 
                            waterLevel.level.toFixed(1);
                    }
                    
                    if (moistureLevel) {
                        document.getElementById('moisture-level').textContent = 
                            moistureLevel.level;
                    }
                }
            } catch (error) {
                console.error('Error updating dashboard:', error);
            }
        }
        
        // Send watering plan
        document.getElementById('plan-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const planType = document.getElementById('plan-type').value;
            const waterVolume = parseInt(document.getElementById('water-volume').value);
            
            let plan = {
                name: `manual_${planType}_plan`,
                plan_type: planType,
                water_volume: waterVolume
            };
            
            if (planType === 'moisture') {
                plan.moisture_threshold = parseFloat(document.getElementById('moisture-threshold').value);
                plan.check_interval = 30;
            } else if (planType === 'time_based') {
                const times = document.getElementById('watering-times').value.split(',');
                plan.weekday_times = times.map(time => ({
                    weekday: 'Monday', // Default to Monday
                    time_water: time.trim()
                }));
                plan.execute_only_once = false;
            }
            
            try {
                const response = await fetch(`${API_BASE}/dashboard/send-plan`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        device_id: currentDevice,
                        plan: plan
                    })
                });
                
                const result = await response.json();
                alert('Plan sent successfully!');
            } catch (error) {
                console.error('Error sending plan:', error);
                alert('Error sending plan');
            }
        });
        
        // Request photo
        async function requestPhoto() {
            try {
                const response = await fetch(`${API_BASE}/dashboard/request-photo`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        device_id: currentDevice,
                        photo_id: `photo_${Date.now()}`
                    })
                });
                
                const result = await response.json();
                alert('Photo request sent!');
            } catch (error) {
                console.error('Error requesting photo:', error);
                alert('Error requesting photo');
            }
        }
        
        // Show/hide form options based on plan type
        document.getElementById('plan-type').addEventListener('change', (e) => {
            const planType = e.target.value;
            document.getElementById('moisture-options').style.display = 
                planType === 'moisture' ? 'block' : 'none';
            document.getElementById('time-options').style.display = 
                planType === 'time_based' ? 'block' : 'none';
        });
        
        // Update dashboard every 30 seconds
        updateDashboard();
        setInterval(updateDashboard, 30000);
    </script>
</body>
</html>
```

## 🔐 Security Considerations

### API Key Management
```python
# Use environment variables for API keys
import os
API_KEY = os.getenv('WATERPLANT_API_KEY')

# Validate API key in middleware
def validate_api_key(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    
    token = auth_header.split(' ')[1]
    return token == API_KEY
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/plan-execution', methods=['POST'])
@limiter.limit("10 per minute")
def post_plan_execution():
    # Implementation
```

### Input Validation
```python
from marshmallow import Schema, fields, validate

class PlanSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    plan_type = fields.Str(required=True, validate=validate.OneOf(['basic', 'moisture', 'time_based']))
    water_volume = fields.Int(required=True, validate=validate.Range(min=50, max=1000))
    moisture_threshold = fields.Float(validate=validate.Range(min=0.1, max=1.0))
    check_interval = fields.Int(validate=validate.Range(min=5, max=1440))

@app.route('/api/dashboard/send-plan', methods=['POST'])
def send_plan():
    schema = PlanSchema()
    try:
        plan = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
```

## 📱 Mobile App Integration

### React Native Example
```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, Button, TextInput, Alert } from 'react-native';

const WaterPlantApp = () => {
    const [waterLevel, setWaterLevel] = useState(0);
    const [moistureLevel, setMoistureLevel] = useState(0);
    const [isConnected, setIsConnected] = useState(false);
    
    const API_BASE = 'https://your-server.com/api';
    const API_KEY = 'your-api-key';
    
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 30000); // Update every 30 seconds
        return () => clearInterval(interval);
    }, []);
    
    const fetchStatus = async () => {
        try {
            const response = await fetch(`${API_BASE}/dashboard/status`, {
                headers: {
                    'Authorization': `Bearer ${API_KEY}`
                }
            });
            const data = await response.json();
            
            if (data.devices.length > 0) {
                const device = data.devices[0];
                setWaterLevel(data.waterLevels[device]?.level || 0);
                setMoistureLevel(data.moistureLevels[device]?.level || 0);
                setIsConnected(true);
            }
        } catch (error) {
            setIsConnected(false);
        }
    };
    
    const sendPlan = async (planType, waterVolume) => {
        try {
            const plan = {
                name: `mobile_${planType}_plan`,
                plan_type: planType,
                water_volume: waterVolume
            };
            
            await fetch(`${API_BASE}/dashboard/send-plan`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${API_KEY}`
                },
                body: JSON.stringify({
                    device_id: 'raspberry-pi-001',
                    plan: plan
                })
            });
            
            Alert.alert('Success', 'Watering plan sent!');
        } catch (error) {
            Alert.alert('Error', 'Failed to send plan');
        }
    };
    
    return (
        <View style={{ padding: 20 }}>
            <Text style={{ fontSize: 24, marginBottom: 20 }}>
                WaterPlantOperator
            </Text>
            
            <Text style={{ color: isConnected ? 'green' : 'red' }}>
                Status: {isConnected ? 'Connected' : 'Disconnected'}
            </Text>
            
            <Text>Water Level: {waterLevel}%</Text>
            <Text>Moisture Level: {moistureLevel}%</Text>
            
            <Button
                title="Water Now (200ml)"
                onPress={() => sendPlan('basic', 200)}
            />
            
            <Button
                title="Smart Water (Moisture-based)"
                onPress={() => sendPlan('moisture', 150)}
            />
        </View>
    );
};

export default WaterPlantApp;
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Dockerfile for server
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  waterplant-server:
    build: .
    ports:
      - "5000:5000"
    environment:
      - API_KEY=your-secure-api-key
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - waterplant-server
    restart: unless-stopped
```

### Cloud Deployment (AWS/GCP/Azure)
```bash
# Deploy to AWS Elastic Beanstalk
eb init waterplant-server
eb create production
eb deploy

# Deploy to Google Cloud Run
gcloud run deploy waterplant-server --source . --platform managed --region us-central1

# Deploy to Azure Container Instances
az container create --resource-group myResourceGroup --name waterplant-server --image your-registry/waterplant-server
```

---

This comprehensive API integration guide provides everything needed to build a complete monitoring and control system for your WaterPlantOperator devices. The modular design allows for easy extension and customization based on your specific requirements.


