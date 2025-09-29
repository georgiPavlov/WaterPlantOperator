#!/usr/bin/env python3
"""
Container Main Application for WaterPlantOperator
Flask API server with mock hardware simulation
"""

import os
import sys
import logging
import json
import time
import threading
import requests
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the run directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import our mock hardware
from mock_hardware import get_hardware_manager

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.container_config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get configuration
config = get_config()

# Device identifier (from original main.py)
DEVICE_GUID = 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e'

# WaterPlantApp backend configuration
WATERPLANTAPP_URL = 'http://host.docker.internal:8001'  # Django server
PUSH_INTERVAL = 5  # seconds
JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5MTc3MDU2LCJpYXQiOjE3NTkxNzM0NTYsImp0aSI6IjIzN2MzZjc1OGUxNjQxN2NiNDQ1MWQxNWI1NDRkYjRmIiwidXNlcl9pZCI6IjEifQ.zJUY2CvisjIwHzQNm2qYtpK9eSHG-cmVrd9P_1-0D3c'

# Create Flask app
app = Flask(__name__)
CORS(app)

# Get hardware manager
hardware_manager = get_hardware_manager()

# Global flag for data pushing
data_pushing_active = False

def push_data_to_waterplantapp():
    """Push sensor data to WaterPlantApp Django server"""
    global data_pushing_active
    
    while data_pushing_active:
        try:
            # Get current sensor readings
            moisture_level = hardware_manager.get_sensor_reading('moisture')
            water_level = hardware_manager.get_sensor_reading('water_level')
            temperature = hardware_manager.get_sensor_reading('temperature')
            humidity = hardware_manager.get_sensor_reading('humidity')
            
            # Convert to percentages for water and moisture
            moisture_percentage = int(moisture_level * 100)
            water_percentage = int(water_level * 100)
            
            # Prepare device data
            device_data = {
                'device_id': DEVICE_GUID,
                'label': 'Container Water Plant Device',
                'water_level': water_percentage,
                'moisture_level': moisture_percentage,
                'water_container_capacity': 2000,
                'send_email': True,
                'is_connected': True
            }
            
            # Push device data to WaterPlantApp
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {JWT_TOKEN}'
                }
                response = requests.post(
                    f'{WATERPLANTAPP_URL}/gadget_communicator_pull/api/create_device',
                    json=device_data,
                    headers=headers,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully pushed device data to WaterPlantApp")
                else:
                    logger.warning(f"Failed to push device data: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Could not connect to WaterPlantApp: {e}")
            
            # Push water level data
            try:
                water_data = {
                    'device': DEVICE_GUID,
                    'water_level': water_percentage
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {JWT_TOKEN}'
                }
                response = requests.post(
                    f'{WATERPLANTAPP_URL}/gadget_communicator_pull/postWater',
                    json=water_data,
                    headers=headers,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully pushed water level: {water_percentage}%")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Could not push water level: {e}")
            
            # Push moisture level data
            try:
                moisture_data = {
                    'device': DEVICE_GUID,
                    'moisture_level': moisture_percentage
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {JWT_TOKEN}'
                }
                response = requests.post(
                    f'{WATERPLANTAPP_URL}/gadget_communicator_pull/postMoisture',
                    json=moisture_data,
                    headers=headers,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully pushed moisture level: {moisture_percentage}%")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Could not push moisture level: {e}")
            
            # Push status data
            try:
                status_data = {
                    'device': DEVICE_GUID,
                    'execution_status': True,
                    'message': 'healthcheck'  # Use HEALTH_CHECK constant to trigger connection status update
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {JWT_TOKEN}'
                }
                response = requests.post(
                    f'{WATERPLANTAPP_URL}/gadget_communicator_pull/postStatus',
                    json=status_data,
                    headers=headers,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully pushed status data")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Could not push status data: {e}")
            
        except Exception as e:
            logger.error(f"Error in data pushing loop: {e}")
        
        # Wait before next push
        time.sleep(PUSH_INTERVAL)

def start_data_pushing():
    """Start the data pushing thread"""
    global data_pushing_active
    if not data_pushing_active:
        data_pushing_active = True
        push_thread = threading.Thread(target=push_data_to_waterplantapp, daemon=True)
        push_thread.start()
        logger.info("Started data pushing to WaterPlantApp")
        return True
    return False

def stop_data_pushing():
    """Stop the data pushing thread"""
    global data_pushing_active
    data_pushing_active = False
    logger.info("Stopped data pushing to WaterPlantApp")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': config.environment,
        'simulation_mode': config.simulation_mode,
        'device_id': DEVICE_GUID
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Get system status"""
    try:
        status = hardware_manager.get_system_info()
        status['device_id'] = DEVICE_GUID
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sensors', methods=['GET'])
def get_sensors():
    """Get sensor readings"""
    try:
        sensors = {
            'moisture': hardware_manager.get_sensor_reading('moisture'),
            'temperature': hardware_manager.get_sensor_reading('temperature'),
            'humidity': hardware_manager.get_sensor_reading('humidity'),
            'water_level': hardware_manager.get_sensor_reading('water_level'),
            'timestamp': datetime.now().isoformat(),
            'device_id': DEVICE_GUID
        }
        return jsonify(sensors)
    except Exception as e:
        logger.error(f"Error getting sensors: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/relays', methods=['GET', 'POST'])
def control_relays():
    """Control relays"""
    try:
        if request.method == 'GET':
            # Get relay states
            relays = {
                name: relay.is_on() 
                for name, relay in hardware_manager.relays.items()
            }
            return jsonify(relays)
        
        elif request.method == 'POST':
            # Control relay
            data = request.get_json()
            relay_name = data.get('relay')
            state = data.get('state', False)
            
            if relay_name in hardware_manager.relays:
                hardware_manager.control_relay(relay_name, state)
                return jsonify({
                    'relay': relay_name,
                    'state': state,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({'error': f'Unknown relay: {relay_name}'}), 400
                
    except Exception as e:
        logger.error(f"Error controlling relays: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/camera/capture', methods=['POST'])
def capture_photo():
    """Take a photo"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename', f'photo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg')
        
        # Ensure filename has .jpg extension
        if not filename.endswith('.jpg'):
            filename += '.jpg'
        
        # Create full path
        photo_path = os.path.join('/app/data', filename)
        
        # Take photo
        success = hardware_manager.take_photo(photo_path)
        
        if success:
            return jsonify({
                'success': True,
                'filename': filename,
                'path': photo_path,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to capture photo'}), 500
            
    except Exception as e:
        logger.error(f"Error capturing photo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/watering/start', methods=['POST'])
def start_watering():
    """Start watering operation"""
    try:
        data = request.get_json() or {}
        duration = data.get('duration', 30)  # seconds
        
        # Turn on pump
        hardware_manager.control_relay('pump', True)
        
        logger.info(f"Started watering for {duration} seconds")
        
        return jsonify({
            'success': True,
            'action': 'watering_started',
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error starting watering: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/watering/stop', methods=['POST'])
def stop_watering():
    """Stop watering operation"""
    try:
        # Turn off pump
        hardware_manager.control_relay('pump', False)
        
        logger.info("Stopped watering")
        
        return jsonify({
            'success': True,
            'action': 'watering_stopped',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error stopping watering: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/config', methods=['GET'])
def get_configuration():
    """Get container configuration"""
    try:
        return jsonify(config.get_config_dict())
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/data-push/start', methods=['POST'])
def start_data_push():
    """Start pushing data to WaterPlantApp"""
    try:
        success = start_data_pushing()
        return jsonify({
            'success': success,
            'message': 'Data pushing started' if success else 'Data pushing already active',
            'target_url': WATERPLANTAPP_URL,
            'interval': PUSH_INTERVAL
        })
    except Exception as e:
        logger.error(f"Error starting data push: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/data-push/stop', methods=['POST'])
def stop_data_push():
    """Stop pushing data to WaterPlantApp"""
    try:
        stop_data_pushing()
        return jsonify({
            'success': True,
            'message': 'Data pushing stopped'
        })
    except Exception as e:
        logger.error(f"Error stopping data push: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/data-push/status', methods=['GET'])
def data_push_status():
    """Get data pushing status"""
    try:
        return jsonify({
            'active': data_pushing_active,
            'target_url': WATERPLANTAPP_URL,
            'interval': PUSH_INTERVAL,
            'device_id': DEVICE_GUID
        })
    except Exception as e:
        logger.error(f"Error getting data push status: {e}")
        return jsonify({'error': str(e)}), 500

# Server Communicator Interface Mock Endpoints
@app.route('/getPlan', methods=['GET'])
def get_plan():
    """Mock getPlan endpoint - returns watering plans"""
    try:
        # Mock plan response
        plan = {
            'name': 'smart_watering',
            'plan_type': 'moisture',
            'water_volume': 150,
            'moisture_threshold': 0.3,
            'device_id': DEVICE_GUID,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(plan)
    except Exception as e:
        logger.error(f"Error getting plan: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/postWater', methods=['POST'])
def post_water():
    """Mock postWater endpoint - receives water level updates"""
    try:
        data = request.get_json()
        water_level = data.get('water_level', 0)
        device_id = data.get('device', DEVICE_GUID)
        
        logger.info(f"Received water level update: {water_level} for device: {device_id}")
        
        return jsonify({
            'success': True,
            'water_level': water_level,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }), 201
    except Exception as e:
        logger.error(f"Error posting water level: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/postMoisture', methods=['POST'])
def post_moisture():
    """Mock postMoisture endpoint - receives moisture level updates"""
    try:
        data = request.get_json()
        moisture_level = data.get('moisture_level', 0)
        device_id = data.get('device', DEVICE_GUID)
        
        logger.info(f"Received moisture level update: {moisture_level} for device: {device_id}")
        
        return jsonify({
            'success': True,
            'moisture_level': moisture_level,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }), 201
    except Exception as e:
        logger.error(f"Error posting moisture level: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/postPhoto', methods=['POST'])
def post_photo():
    """Mock postPhoto endpoint - receives photo uploads"""
    try:
        # Handle multipart form data
        if 'image_file' in request.files:
            photo_file = request.files['image_file']
            device_id = request.form.get('device_id', DEVICE_GUID)
            photo_id = request.form.get('photo_id', 'unknown')
            
            # Save photo to data directory
            filename = f"{photo_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            photo_path = os.path.join('/app/data', filename)
            photo_file.save(photo_path)
            
            logger.info(f"Received photo upload: {filename} for device: {device_id}")
            
            return jsonify({
                'success': True,
                'photo_id': photo_id,
                'filename': filename,
                'device_id': device_id,
                'timestamp': datetime.now().isoformat()
            }), 201
        else:
            return jsonify({'error': 'No image file provided'}), 400
    except Exception as e:
        logger.error(f"Error posting photo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/getPhoto', methods=['GET'])
def get_photo():
    """Mock getPhoto endpoint - returns photo capture requests"""
    try:
        device_id = request.args.get('device', DEVICE_GUID)
        
        # Mock photo request
        photo_request = {
            'action': 'capture_photo',
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(photo_request)
    except Exception as e:
        logger.error(f"Error getting photo request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/postStatus', methods=['POST'])
def post_status():
    """Mock postStatus endpoint - receives plan execution status"""
    try:
        data = request.get_json()
        execution_status = data.get('execution_status', False)
        message = data.get('message', '')
        device_id = data.get('device', DEVICE_GUID)
        
        logger.info(f"Received status update: {message} (success: {execution_status}) for device: {device_id}")
        
        return jsonify({
            'success': True,
            'execution_status': execution_status,
            'message': message,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }), 201
    except Exception as e:
        logger.error(f"Error posting status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/getWaterLevel', methods=['GET'])
def get_water_level():
    """Mock getWaterLevel endpoint - returns water level reset requests"""
    try:
        device_id = request.args.get('device', DEVICE_GUID)
        
        # Mock water level reset request
        water_request = {
            'action': 'reset_water_level',
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(water_request)
    except Exception as e:
        logger.error(f"Error getting water level request: {e}")
        return jsonify({'error': str(e)}), 500

# Vue App Compatible Endpoints (Django REST Framework style)
@app.route('/gadget_communicator_pull/api/list_devices', methods=['GET'])
def list_devices():
    """List devices - compatible with Vue app"""
    try:
        # Get current sensor readings for real-time data
        current_moisture = hardware_manager.get_sensor_reading('moisture')
        current_water_level = hardware_manager.get_sensor_reading('water_level')
        
        # Convert to percentages for display
        moisture_percentage = int(current_moisture * 100)
        water_percentage = int(current_water_level * 100)
        
        # Mock device list with real-time sensor data
        devices = [{
            'device_id': DEVICE_GUID,
            'label': 'Container Water Plant Device',
            'water_level': water_percentage,
            'moisture_level': moisture_percentage,
            'water_container_capacity': 2000,
            'send_email': True,
            'is_connected': True,  # Always connected when container is running
            'id': 1
        }]
        
        logger.info(f"Returning device list with moisture: {moisture_percentage}%, water: {water_percentage}%")
        return jsonify(devices)
    except Exception as e:
        logger.error(f"Error listing devices: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gadget_communicator_pull/api/create_device', methods=['POST'])
def create_device():
    """Create device - compatible with Vue app"""
    try:
        data = request.get_json()
        device = {
            'device_id': data.get('device_id', f'device_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
            'label': data.get('label', 'New Device'),
            'water_level': 100,
            'moisture_level': 0,
            'water_container_capacity': data.get('water_container_capacity', 2000),
            'send_email': data.get('send_email', False),
            'is_connected': False,
            'id': int(datetime.now().timestamp())
        }
        logger.info(f"Created device: {device}")
        return jsonify(device), 201
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gadget_communicator_pull/api/delete_device/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete device - compatible with Vue app"""
    try:
        logger.info(f"Deleted device: {device_id}")
        return jsonify({'success': True, 'message': f'Device {device_id} deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gadget_communicator_pull/api/update_device', methods=['POST'])
def update_device():
    """Update device - compatible with Vue app"""
    try:
        data = request.get_json()
        logger.info(f"Updated device: {data}")
        return jsonify({'success': True, 'message': 'Device updated'}), 200
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gadget_communicator_pull/api/list_device_charts/<device_id>', methods=['GET'])
def list_device_charts(device_id):
    """List device water charts - compatible with Vue app"""
    try:
        # Get current sensor readings for real-time chart data
        current_moisture = hardware_manager.get_sensor_reading('moisture')
        current_water_level = hardware_manager.get_sensor_reading('water_level')
        
        # Convert to percentages
        moisture_percentage = int(current_moisture * 100)
        water_percentage = int(current_water_level * 100)
        
        # Mock water chart data with real-time values
        charts = [{
            'id': 1,
            'device_id': device_id,
            'water_level': water_percentage,
            'moisture_level': moisture_percentage,
            'timestamp': datetime.now().isoformat(),
            'recorded_at': datetime.now().isoformat()
        }]
        return jsonify(charts)
    except Exception as e:
        logger.error(f"Error listing device charts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gadget_communicator_pull/api/device_status/<device_id>', methods=['GET'])
def device_status(device_id):
    """Get device connection status - for Vue app compatibility"""
    try:
        if device_id == DEVICE_GUID:
            return jsonify({
                'device_id': device_id,
                'is_connected': True,
                'status': 'online',
                'last_seen': datetime.now().isoformat(),
                'message': 'Device is connected and operational'
            })
        else:
            return jsonify({
                'device_id': device_id,
                'is_connected': False,
                'status': 'offline',
                'last_seen': None,
                'message': 'Device not found'
            }), 404
    except Exception as e:
        logger.error(f"Error getting device status: {e}")
        return jsonify({'error': str(e)}), 500

# Authentication Endpoints (Vue App Compatible)
@app.route('/api-token-auth/', methods=['POST'])
def api_token_auth():
    """Mock JWT authentication endpoint - compatible with Vue app"""
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Mock authentication - accept any credentials for demo
        if username and password:
            # Mock JWT token
            mock_token = f"mock_jwt_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            return jsonify({
                'access': mock_token,
                'refresh': f"mock_refresh_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Error in authentication: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function"""
    logger.info("Starting WaterPlantOperator Container API Server...")
    logger.info(f"Environment: {config.environment}")
    logger.info(f"Simulation Mode: {config.simulation_mode}")
    logger.info(f"API Host: {config.api_host}")
    logger.info(f"API Port: {config.api_port}")
    logger.info(f"WaterPlantApp URL: {WATERPLANTAPP_URL}")
    logger.info(f"Push Interval: {PUSH_INTERVAL} seconds")
    
    # Create data directory if it doesn't exist
    os.makedirs('/app/data', exist_ok=True)
    
    # Start data pushing to WaterPlantApp
    logger.info("Starting data pushing to WaterPlantApp...")
    start_data_pushing()
    
    # Start Flask server
    app.run(
        host=config.api_host,
        port=config.api_port,
        debug=False
    )

if __name__ == '__main__':
    main()
