"""
Pytest configuration and shared fixtures for WaterPlantOperator tests.
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from datetime import datetime, date

# Add the run directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'run'))

# Mock hardware dependencies for non-Raspberry Pi systems
try:
    import picamera
except ImportError:
    # Create mock picamera module
    class MockPiCamera:
        def __init__(self):
            self.start_preview = Mock()
            self.stop_preview = Mock()
            self.capture = Mock()
    
    mock_picamera = type('MockModule', (), {'PiCamera': MockPiCamera})()
    sys.modules['picamera'] = mock_picamera

# Mock gpiozero for non-Raspberry Pi systems
import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'

try:
    from gpiozero import OutputDevice, LightSensor
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device
    
    # Set the pin factory to mock
    Device.pin_factory = MockFactory()
    
except ImportError:
    # Create mock gpiozero classes
    class MockOutputDevice:
        def __init__(self, pin, active_high=True, **kwargs):
            self.pin = pin
            self.active_high = active_high
            self.on = Mock()
            self.off = Mock()
            self.value = False
            self.is_active = Mock(return_value=False)
    
    class MockLightSensor:
        def __init__(self, pin=None, **kwargs):
            self.pin = pin
            self.value = 0.5
            self.wait_for_light = Mock()
            self.wait_for_dark = Mock()
            self.when_light = Mock()
            self.when_dark = Mock()
            self.is_active = Mock(return_value=True)
    
    # Replace the actual classes with mocks
    import run.sensor.relay
    import run.sensor.moisture_sensor
    run.sensor.relay.OutputDevice = MockOutputDevice
    run.sensor.moisture_sensor.LightSensor = MockLightSensor

@pytest.fixture
def mock_relay():
    """Mock relay sensor for testing."""
    relay = Mock()
    relay.on = Mock()
    relay.off = Mock()
    return relay

@pytest.fixture
def mock_moisture_sensor():
    """Mock moisture sensor for testing."""
    moisture = Mock()
    moisture.value = 0.3  # Default moisture value (30% dry)
    moisture.is_dry = Mock(return_value=True)
    return moisture

@pytest.fixture
def mock_camera():
    """Mock camera for testing."""
    camera = Mock()
    camera.take_photo = Mock()
    return camera

@pytest.fixture
def mock_pi_camera():
    """Mock PiCamera instance for testing."""
    camera = Mock()
    camera.start_preview = Mock()
    camera.stop_preview = Mock()
    camera.capture = Mock()
    return camera

@pytest.fixture
def mock_server_communicator():
    """Mock server communicator for testing."""
    communicator = Mock()
    communicator.get_plan = Mock(return_value={})
    communicator.post_water = Mock(return_value={})
    communicator.post_moisture = Mock(return_value={})
    communicator.post_picture = Mock(return_value={})
    communicator.post_plan_execution = Mock(return_value={})
    communicator.get_water_level = Mock(return_value={})
    communicator.get_picture = Mock(return_value={})
    communicator.return_emply_json = Mock(return_value={})
    return communicator

@pytest.fixture
def sample_plan_data():
    """Sample plan data for testing."""
    return {
        "name": "test_plan",
        "plan_type": "basic",
        "water_volume": 200
    }

@pytest.fixture
def sample_moisture_plan_data():
    """Sample moisture plan data for testing."""
    return {
        "name": "moisture_plan",
        "plan_type": "moisture",
        "water_volume": 150,
        "moisture_threshold": 0.4,
        "check_interval": 30
    }

@pytest.fixture
def sample_time_plan_data():
    """Sample time plan data for testing."""
    return {
        "name": "time_plan",
        "plan_type": "time_based",
        "water_volume": 100,
        "weekday_times": [
            {"weekday": "Monday", "time_water": "08:00"},
            {"weekday": "Friday", "time_water": "18:00"}
        ],
        "execute_only_once": False
    }

@pytest.fixture
def mock_time_keeper():
    """Mock time keeper for testing."""
    time_keeper = Mock()
    time_keeper.get_current_time = Mock(return_value="10:00")
    time_keeper.get_current_date = Mock(return_value=date.today())
    time_keeper.get_current_time_minus_delta = Mock(return_value="09:30")
    time_keeper.get_time_from_time_string = Mock(return_value="08:00")
    time_keeper.set_time_last_watered = Mock()
    time_keeper.set_date_last_watered = Mock()
    time_keeper.time_last_watered = "09:00"
    time_keeper.date_last_watered = date.today()
    return time_keeper
