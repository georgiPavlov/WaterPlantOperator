"""
Unit tests for Status model.
"""
import pytest
from run.model.status import Status, MESSAGE_INSUFFICIENT_WATER, MESSAGE_SUCCESS_MOISTURE, MESSAGE_SUCCESS_TIMER, MESSAGE_INVALID_PLAN, MESSAGE_DELETED_PLAN, MESSAGE_SUFFICIENT_WATER, MESSAGE_PLAN_CONDITION_NOT_MET, MESSAGE_BASIC_PLAN_SUCCESS, HEALTH_CHECK


class TestStatus:
    """Test cases for Status class."""

    def test_status_initialization(self):
        """Test status initialization with watering status and message."""
        watering_status = True
        message = "Test message"
        
        status = Status(watering_status, message)
        
        assert status.watering_status == watering_status
        assert status.message == message

    def test_status_with_success(self):
        """Test status with successful watering."""
        status = Status(True, MESSAGE_SUCCESS_MOISTURE)
        
        assert status.watering_status == True
        assert status.message == MESSAGE_SUCCESS_MOISTURE

    def test_status_with_failure(self):
        """Test status with failed watering."""
        status = Status(False, MESSAGE_INSUFFICIENT_WATER)
        
        assert status.watering_status == False
        assert status.message == MESSAGE_INSUFFICIENT_WATER

    def test_status_with_different_messages(self):
        """Test status with different predefined messages."""
        messages = [
            MESSAGE_INSUFFICIENT_WATER,
            MESSAGE_SUCCESS_MOISTURE,
            MESSAGE_SUCCESS_TIMER,
            MESSAGE_INVALID_PLAN,
            MESSAGE_DELETED_PLAN,
            MESSAGE_SUFFICIENT_WATER,
            MESSAGE_PLAN_CONDITION_NOT_MET,
            MESSAGE_BASIC_PLAN_SUCCESS,
            HEALTH_CHECK
        ]
        
        for message in messages:
            status = Status(True, message)
            assert status.message == message

    def test_status_boolean_values(self):
        """Test status with different boolean values."""
        # Test with True
        status_true = Status(True, "Success")
        assert status_true.watering_status == True
        
        # Test with False
        status_false = Status(False, "Failure")
        assert status_false.watering_status == False

    def test_status_message_constants(self):
        """Test that all message constants are defined and have expected values."""
        assert MESSAGE_INSUFFICIENT_WATER == "[Insufficient water in the container]"
        assert MESSAGE_SUCCESS_MOISTURE == "[Plant successfully watered with moisture plan]"
        assert MESSAGE_SUCCESS_TIMER == "[Plant successfully watered with timer plan]"
        assert MESSAGE_INVALID_PLAN == "[Invalid plan]"
        assert MESSAGE_DELETED_PLAN == "[Watering plan deleted]"
        assert MESSAGE_SUFFICIENT_WATER == "[Sufficient water in the container]"
        assert MESSAGE_PLAN_CONDITION_NOT_MET == "[Plan condition not met]"
        assert MESSAGE_BASIC_PLAN_SUCCESS == "[Successful watering of plant]"
        assert HEALTH_CHECK == "healthcheck"

    def test_status_new_methods(self):
        """Test new methods added to Status class."""
        success_status = Status(True, "Operation successful")
        failure_status = Status(False, "Operation failed")
        
        # Test __str__ method
        success_str = str(success_status)
        assert "✓" in success_str
        assert "Operation successful" in success_str
        
        failure_str = str(failure_status)
        assert "✗" in failure_str
        assert "Operation failed" in failure_str
        
        # Test __bool__ method
        assert bool(success_status) is True
        assert bool(failure_status) is False
        
        # Test to_dict method
        success_dict = success_status.to_dict()
        assert success_dict == {
            'watering_status': True,
            'message': 'Operation successful'
        }
        
        # Test class methods
        success_from_method = Status.success("Test success")
        assert success_from_method.watering_status is True
        assert success_from_method.message == "Test success"
        
        failure_from_method = Status.failure("Test failure")
        assert failure_from_method.watering_status is False
        assert failure_from_method.message == "Test failure"

    def test_status_validation(self):
        """Test Status class validation."""
        # Test with invalid watering_status
        with pytest.raises(TypeError):
            Status("not_a_bool", "message")
        
        # Test with empty message
        with pytest.raises(ValueError):
            Status(True, "")
        
        # Test with non-string message
        with pytest.raises(ValueError):
            Status(True, None)
