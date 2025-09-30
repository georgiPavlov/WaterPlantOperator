"""
Unit tests for Device model.
"""
import pytest
import json
from run.model.device import Device


class TestDevice:
    """Test cases for Device class."""

    def test_device_initialization(self):
        """Test device initialization with device_id."""
        device_id = "test-device-123"
        device = Device(device_id)
        
        assert device.device_id == device_id

    def test_device_from_json(self):
        """Test creating device from JSON string."""
        device_id = "test-device-456"
        json_string = json.dumps({"device_id": device_id})
        
        device = Device.from_json(json_string)
        
        assert device.device_id == device_id

    def test_device_from_json_invalid(self):
        """Test creating device from invalid JSON."""
        invalid_json = "invalid json string"
        
        with pytest.raises(json.JSONDecodeError):
            Device.from_json(invalid_json)

    def test_device_repr(self):
        """Test device string representation."""
        device_id = "test-device-789"
        device = Device(device_id)
        
        expected_repr = f'<device_id {device_id}>'
        assert repr(device) == expected_repr

    def test_device_from_json_missing_field(self):
        """Test creating device from JSON missing required field."""
        json_string = json.dumps({"name": "test"})  # Missing device_id
        
        with pytest.raises(TypeError):
            Device.from_json(json_string)

