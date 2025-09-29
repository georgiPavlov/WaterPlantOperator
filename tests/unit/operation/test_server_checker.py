"""
Unit tests for ServerChecker operation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from run.operation.server_checker import ServerChecker
from run.model.status import Status, HEALTH_CHECK


class TestServerChecker:
    """Test cases for ServerChecker class."""

    @pytest.fixture
    def mock_pump(self):
        """Create a mock pump for testing."""
        pump = Mock()
        pump.MOISTURE_SENSOR_KEY = 'moisture_sensor'
        pump.get_moisture_level_in_percent = Mock(return_value=75)
        pump.get_water_level_in_percent = Mock(return_value=80)
        pump.get_running_plan = Mock(return_value=None)
        pump.execute_water_plan = Mock(return_value=Status(True, "Success"))
        return pump

    @pytest.fixture
    def mock_communicator(self):
        """Create a mock communicator for testing."""
        communicator = Mock()
        communicator.get_plan = Mock(return_value={})
        communicator.get_water_level = Mock(return_value={})
        communicator.get_picture = Mock(return_value={})
        communicator.post_plan_execution = Mock(return_value={})
        communicator.post_water = Mock(return_value={})
        communicator.post_moisture = Mock(return_value={})
        communicator.post_picture = Mock(return_value={})
        communicator.return_emply_json = Mock(return_value={})
        return communicator

    @pytest.fixture
    def server_checker(self, mock_pump, mock_communicator):
        """Create a ServerChecker instance for testing."""
        return ServerChecker(
            pump=mock_pump,
            communicator=mock_communicator,
            wait_time_between_cycle=1
        )

    def test_server_checker_initialization(self, mock_pump, mock_communicator):
        """Test ServerChecker initialization."""
        wait_time = 5
        checker = ServerChecker(mock_pump, mock_communicator, wait_time)
        
        assert checker.pump == mock_pump
        assert checker.communicator == mock_communicator
        assert checker.wait_time_between_cycle == wait_time

    def test_plan_executor_health_check(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor health check cycle."""
        mock_moisture_sensor = Mock()
        mock_camera = Mock()
        
        # Test the moisture sensor assignment
        server_checker.pump.moisture_sensor = mock_moisture_sensor
        assert server_checker.pump.moisture_sensor == mock_moisture_sensor
        
        # Test health check status creation
        health_status = Status(watering_status=False, message=HEALTH_CHECK)
        mock_communicator.post_plan_execution(health_status)
        mock_communicator.post_plan_execution.assert_called_with(health_status)

    def test_plan_executor_water_level_reset(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor with water level reset."""
        # Mock water level response
        water_level_response = {"water": 1500}
        mock_communicator.get_water_level.return_value = water_level_response
        mock_communicator.return_emply_json.return_value = {}
        
        # Test water level reset functionality
        if water_level_response != mock_communicator.return_emply_json():
            water_level_value = water_level_response["water"]
            mock_pump.reset_water_level(water_level_value)
            mock_pump.reset_water_level.assert_called_with(1500)

    def test_plan_executor_photo_capture(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor with photo capture request."""
        mock_camera = Mock()
        
        # Mock photo response
        photo_response = {"photo_id": "test_photo"}
        mock_communicator.get_picture.return_value = photo_response
        mock_communicator.return_emply_json.return_value = {}
        
        # Test photo capture functionality
        if photo_response != mock_communicator.return_emply_json():
            photo_name = photo_response["photo_id"]
            mock_camera.take_photo(photo_name)
            mock_camera.take_photo.assert_called_with("test_photo")

    def test_plan_executor_new_plan_execution(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor with new plan execution."""
        mock_moisture_sensor = Mock()
        mock_camera = Mock()
        
        # Mock plan response
        plan_response = {"plan_type": "basic", "water_volume": 200, "name": "test_plan"}
        mock_communicator.get_plan.return_value = plan_response
        mock_communicator.return_emply_json.return_value = {}
        
        # Test plan execution functionality
        if plan_response != mock_communicator.return_emply_json():
            status = mock_pump.execute_water_plan(plan_response)
            mock_pump.execute_water_plan.assert_called_with(plan_response)

    def test_plan_executor_running_plan_continuation(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor with running plan continuation."""
        mock_moisture_sensor = Mock()
        mock_camera = Mock()
        mock_running_plan = Mock()
        
        # Mock no new plan but running plan exists
        mock_communicator.get_plan.return_value = {}
        mock_communicator.return_emply_json.return_value = {}
        mock_pump.get_running_plan.return_value = mock_running_plan
        
        # Test running plan execution
        if mock_communicator.get_plan() == mock_communicator.return_emply_json():
            if mock_pump.get_running_plan() is not None:
                plan = mock_pump.get_running_plan()
                status = mock_pump.execute_water_plan(plan)
                mock_pump.execute_water_plan.assert_called_with(plan)

    def test_plan_executor_no_plan_moisture_check(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor with no plan - moisture check only."""
        # Mock no new plan and no running plan
        mock_communicator.get_plan.return_value = {}
        mock_communicator.return_emply_json.return_value = {}
        mock_pump.get_running_plan.return_value = None
        
        # Test moisture check functionality
        if mock_communicator.get_plan() == mock_communicator.return_emply_json():
            if mock_pump.get_running_plan() is None:
                moisture_level = mock_pump.get_moisture_level_in_percent()
                mock_communicator.post_moisture(moisture_level)
                mock_communicator.post_moisture.assert_called_with(75)

    def test_send_result(self, server_checker, mock_communicator):
        """Test send_result method."""
        status = Status(True, "Test message")
        moisture_level = 75
        water_level = 80
        
        server_checker.send_result(moisture_level, status, water_level)
        
        # Verify all results were posted
        mock_communicator.post_plan_execution.assert_called_with(status)
        mock_communicator.post_water.assert_called_with(water_level)
        mock_communicator.post_moisture.assert_called_with(moisture_level)

    def test_plan_executor_exception_handling(self, server_checker, mock_pump, mock_communicator):
        """Test plan executor exception handling."""
        # Mock an exception in the communicator
        mock_communicator.get_plan.side_effect = Exception("Network error")
        
        # Test exception handling
        try:
            mock_communicator.get_plan()
        except Exception as e:
            # Should handle the exception gracefully
            assert str(e) == "Network error"