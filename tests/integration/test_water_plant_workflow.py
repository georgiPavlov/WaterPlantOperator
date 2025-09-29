"""
Integration tests for the complete water plant workflow.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
import json

# Import the main components
from run.operation.pump import Pump
from run.operation.server_checker import ServerChecker
from run.http_communicator.server_communicator import ServerCommunicator
from run.email_sender.sender import Sender
from run.model.plan import Plan
from run.model.moisture_plan import MoisturePlan
from run.model.time_plan import TimePlan
from run.model.status import Status
from run.common.time_keeper import TimeKeeper


class TestWaterPlantWorkflow:
    """Integration tests for the complete water plant system."""

    @pytest.fixture
    def mock_relay(self):
        """Mock relay for testing."""
        relay = Mock()
        relay.on = Mock()
        relay.off = Mock()
        relay.is_active = Mock(return_value=False)
        return relay

    @pytest.fixture
    def mock_moisture_sensor(self):
        """Mock moisture sensor for testing."""
        sensor = Mock()
        sensor.value = 0.5  # 50% moisture
        sensor.wait_for_dry = Mock()
        sensor.wait_for_wet = Mock()
        return sensor

    @pytest.fixture
    def mock_camera(self):
        """Mock camera for testing."""
        camera = Mock()
        camera.take_photo = Mock()
        return camera

    @pytest.fixture
    def mock_communicator(self):
        """Mock server communicator for testing."""
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
    def pump(self):
        """Create a pump instance for testing."""
        return Pump(water_max_capacity=3000, water_pumped_in_second=10, moisture_max_level=100)

    @pytest.fixture
    def server_checker(self, pump, mock_communicator):
        """Create a server checker instance for testing."""
        return ServerChecker(pump, mock_communicator, wait_time_between_cycle=1)

    def test_basic_watering_workflow(self, pump, mock_relay):
        """Test the complete basic watering workflow."""
        # Create a basic plan
        plan_data = {
            "plan_type": "basic",
            "water_volume": 200,
            "name": "basic_test_plan"
        }
        
        # Execute the plan
        with patch('run.operation.pump.time.sleep'):
            result = pump.execute_water_plan(plan_data, relay=mock_relay)
        
        # Verify the workflow
        assert result.watering_status is True
        assert "success" in result.message.lower()
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()

    def test_moisture_based_watering_workflow(self, pump, mock_relay, mock_moisture_sensor):
        """Test the complete moisture-based watering workflow."""
        # Create a moisture plan
        plan_data = {
            "plan_type": "moisture",
            "water_volume": 150,
            "moisture_threshold": 0.3,
            "check_interval": 30,
            "name": "moisture_test_plan"
        }
        
        # Set up moisture sensor to trigger watering
        mock_moisture_sensor.value = 0.2  # 20% moisture (below threshold)
        
        # Execute the plan
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"  # More than 30 minutes ago
                mock_get_time.return_value = mock_time_keeper
                
                result = pump.execute_water_plan(plan_data, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
        
        # Verify the workflow
        assert result.watering_status is True
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()

    def test_time_based_watering_workflow(self, pump, mock_relay):
        """Test the complete time-based watering workflow."""
        # Create a time-based plan
        plan_data = {
            "plan_type": "time_based",
            "water_volume": 180,
            "weekday_times": [
                {"weekday": "Monday", "time_water": "10:00"},
                {"weekday": "Wednesday", "time_water": "14:00"}
            ],
            "execute_only_once": False,
            "name": "time_test_plan"
        }
        
        # Execute the plan
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time, \
                 patch('run.operation.pump.date') as mock_date, \
                 patch('run.operation.pump.calendar') as mock_calendar:
                
                # Mock current time as Monday 10:00
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"
                mock_get_time.return_value = mock_time_keeper
                
                mock_date.today.return_value = date(2023, 1, 16)  # Monday
                mock_calendar.day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                
                result = pump.execute_water_plan(plan_data, relay=mock_relay)
        
        # Verify the workflow
        assert result.watering_status is True
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()

    def test_server_communication_workflow(self, server_checker, mock_communicator, mock_relay, mock_moisture_sensor, mock_camera):
        """Test the complete server communication workflow."""
        # Mock server responses
        mock_communicator.get_plan.return_value = {
            "plan_type": "basic",
            "water_volume": 200,
            "name": "server_plan"
        }
        mock_communicator.get_water_level.return_value = {"water": 1000}
        mock_communicator.get_picture.return_value = {"photo_id": "test_photo"}
        
        # Test the workflow components
        # 1. Get plan from server
        plan = mock_communicator.get_plan()
        assert plan["plan_type"] == "basic"
        
        # 2. Execute plan
        with patch('run.operation.pump.time.sleep'):
            result = server_checker.pump.execute_water_plan(plan, relay=mock_relay)
        
        # 3. Send results back to server
        server_checker.send_result(75, result, 80)
        
        # Verify all communications
        mock_communicator.get_plan.assert_called()
        mock_communicator.post_plan_execution.assert_called()
        mock_communicator.post_water.assert_called_with(80)
        mock_communicator.post_moisture.assert_called_with(75)

    def test_water_level_management_workflow(self, pump):
        """Test the complete water level management workflow."""
        # Test initial water level
        initial_level = pump.get_water_level_in_percent()
        assert 0 <= initial_level <= 100
        
        # Test water level reset
        pump.reset_water_level(2000)
        new_level = pump.get_water_level_in_percent()
        assert new_level > initial_level
        
        # Test water level sufficiency check
        is_sufficient = pump.is_water_level_sufficient(100)
        assert isinstance(is_sufficient, bool)

    def test_moisture_monitoring_workflow(self, pump, mock_moisture_sensor):
        """Test the complete moisture monitoring workflow."""
        # Set up moisture sensor
        pump.moisture_sensor = mock_moisture_sensor
        
        # Test moisture level reading
        moisture_level = pump.get_moisture_level_in_percent()
        assert 0 <= moisture_level <= 100
        
        # Test moisture-based watering decision
        mock_moisture_sensor.value = 0.2  # Low moisture
        low_moisture_level = pump.get_moisture_level_in_percent()
        assert low_moisture_level < 50

    def test_error_handling_workflow(self, pump, mock_relay):
        """Test error handling in the watering workflow."""
        # Test with invalid plan
        invalid_plan = {"plan_type": "invalid", "name": "invalid_plan"}
        result = pump.execute_water_plan(invalid_plan, relay=mock_relay)
        assert result.watering_status is False
        assert "invalid" in result.message.lower()
        
        # Test with insufficient water
        large_plan = {
            "plan_type": "basic",
            "water_volume": 5000,  # Very large volume
            "name": "large_plan"
        }
        result = pump.execute_water_plan(large_plan, relay=mock_relay)
        assert result.watering_status is False
        assert "insufficient" in result.message.lower()

    def test_plan_execution_priority_workflow(self, pump, mock_relay):
        """Test plan execution priority and conflict resolution."""
        # Test plan deletion
        delete_plan = {"plan_type": "delete", "name": "delete_plan"}
        result = pump.execute_water_plan(delete_plan, relay=mock_relay)
        assert result.watering_status is False
        assert "deleted" in result.message.lower()
        
        # Test running plan management
        running_plan = pump.get_running_plan()
        assert running_plan is None  # No plan should be running initially

    def test_time_management_workflow(self):
        """Test time management and scheduling workflow."""
        time_keeper = TimeKeeper("10:00")
        
        # Test time setting and retrieval
        test_time = "14:30"
        time_keeper.set_time_last_watered(test_time)
        assert time_keeper.time_last_watered == test_time
        
        # Test date management
        test_date = date(2023, 1, 15)
        time_keeper.set_date_last_watered(test_date)
        assert time_keeper.date_last_watered == test_date
        
        # Test time calculations
        current_time = TimeKeeper.get_current_time()
        assert isinstance(current_time, str)
        assert len(current_time) == 5  # HH:MM format
        
        # Test time delta calculations
        delta_time = TimeKeeper.get_current_time_minus_delta(60)  # 1 hour ago
        assert isinstance(delta_time, str)

    def test_communication_error_handling_workflow(self, server_checker, mock_communicator):
        """Test communication error handling workflow."""
        # Test network error handling
        mock_communicator.get_plan.side_effect = Exception("Network error")
        
        try:
            mock_communicator.get_plan()
        except Exception as e:
            assert str(e) == "Network error"
        
        # Test server error responses
        mock_communicator.get_plan.side_effect = None
        mock_communicator.get_plan.return_value = {}  # Empty response
        
        plan = mock_communicator.get_plan()
        assert plan == {}

    def test_complete_system_integration(self, server_checker, mock_communicator, mock_relay, mock_moisture_sensor, mock_camera):
        """Test the complete system integration workflow."""
        # Mock a complete server interaction cycle
        mock_communicator.get_plan.return_value = {
            "plan_type": "moisture",
            "water_volume": 150,
            "moisture_threshold": 0.4,
            "check_interval": 30,
            "name": "integration_plan"
        }
        
        # Set up sensors
        server_checker.pump.moisture_sensor = mock_moisture_sensor
        mock_moisture_sensor.value = 0.3  # Below threshold
        
        # Execute the complete workflow
        with patch('run.operation.pump.time.sleep'):
            with patch.object(server_checker.pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"
                mock_get_time.return_value = mock_time_keeper
                
                # Get plan from server
                plan = mock_communicator.get_plan()
                
                # Execute plan
                result = server_checker.pump.execute_water_plan(plan, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
                
                # Send results back
                server_checker.send_result(70, result, 85)
        
        # Verify complete workflow
        assert result.watering_status is True
        mock_communicator.get_plan.assert_called()
        mock_communicator.post_plan_execution.assert_called()
        mock_communicator.post_water.assert_called_with(85)
        mock_communicator.post_moisture.assert_called_with(70)
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()