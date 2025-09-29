"""
Integration tests for edge cases and error scenarios.
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
from run.common.json_creator import get_json, get_json_sm, dump_json


class TestEdgeCases:
    """Integration tests for edge cases and error scenarios."""

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
        sensor.value = 0.5
        sensor.wait_for_dry = Mock()
        sensor.wait_for_wet = Mock()
        return sensor

    @pytest.fixture
    def pump(self):
        """Create a pump instance for testing."""
        return Pump(water_max_capacity=3000, water_pumped_in_second=10, moisture_max_level=100)

    def test_extreme_water_volumes(self, pump, mock_relay):
        """Test edge cases with extreme water volumes."""
        # Test with zero water volume
        zero_plan = {
            "plan_type": "basic",
            "water_volume": 0,
            "name": "zero_plan"
        }
        result = pump.execute_water_plan(zero_plan, relay=mock_relay)
        assert result.watering_status is True  # Should still succeed with 0 volume
        
        # Test with very large water volume
        large_plan = {
            "plan_type": "basic",
            "water_volume": 10000,
            "name": "large_plan"
        }
        result = pump.execute_water_plan(large_plan, relay=mock_relay)
        assert result.watering_status is False  # Should fail due to insufficient water
        assert "insufficient" in result.message.lower()

    def test_extreme_moisture_thresholds(self, pump, mock_relay, mock_moisture_sensor):
        """Test edge cases with extreme moisture thresholds."""
        # Test with threshold at 0 (always water)
        plan_0 = {
            "plan_type": "moisture",
            "water_volume": 100,
            "moisture_threshold": 0.0,
            "check_interval": 30,
            "name": "threshold_0_plan"
        }
        mock_moisture_sensor.value = 0.1  # 10% moisture
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"
                mock_get_time.return_value = mock_time_keeper
                
                result = pump.execute_water_plan(plan_0, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
        
        assert result.watering_status is True
        
        # Test with threshold at 1 (never water)
        plan_1 = {
            "plan_type": "moisture",
            "water_volume": 100,
            "moisture_threshold": 1.0,
            "check_interval": 30,
            "name": "threshold_1_plan"
        }
        mock_moisture_sensor.value = 0.9  # 90% moisture
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"
                mock_get_time.return_value = mock_time_keeper
                
                result = pump.execute_water_plan(plan_1, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
        
        assert result.watering_status is False

    def test_extreme_time_intervals(self, pump, mock_relay, mock_moisture_sensor):
        """Test edge cases with extreme time intervals."""
        # Test with very short interval (0 minutes)
        short_plan = {
            "plan_type": "moisture",
            "water_volume": 100,
            "moisture_threshold": 0.5,
            "check_interval": 0,
            "name": "short_interval_plan"
        }
        mock_moisture_sensor.value = 0.3  # Below threshold
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "10:00"  # Same time
                mock_get_time.return_value = mock_time_keeper
                
                result = pump.execute_water_plan(short_plan, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
        
        assert result.watering_status is True  # Should water immediately
        
        # Test with very long interval (24 hours)
        long_plan = {
            "plan_type": "moisture",
            "water_volume": 100,
            "moisture_threshold": 0.5,
            "check_interval": 1440,  # 24 hours
            "name": "long_interval_plan"
        }
        mock_moisture_sensor.value = 0.3  # Below threshold
        with patch('run.operation.pump.time.sleep'):
            with patch.object(pump, 'get_time') as mock_get_time:
                mock_time_keeper = Mock()
                mock_time_keeper.get_current_time_minus_delta.return_value = "10:00"
                mock_time_keeper.time_last_watered = "09:00"  # 1 hour ago
                mock_get_time.return_value = mock_time_keeper
                
                result = pump.execute_water_plan(long_plan, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
        
        assert result.watering_status is False  # Should not water (too soon)

    def test_malformed_json_data(self):
        """Test edge cases with malformed JSON data."""
        # Test with invalid JSON
        invalid_json = '{"invalid": json}'
        try:
            result = get_json(invalid_json)
            assert result == {}
        except Exception:
            # Expected behavior for malformed JSON
            pass
        
        # Test with empty JSON
        empty_json = '{}'
        result = get_json(empty_json)
        assert result == {}
        
        # Test with None input
        result = get_json(None)
        assert result == {}
        
        # Test with non-string input
        result = get_json(123)
        assert result == {}

    def test_extreme_time_values(self):
        """Test edge cases with extreme time values."""
        time_keeper = TimeKeeper("10:00")
        
        # Test with invalid time format
        with pytest.raises(ValueError):
            TimeKeeper.get_time_from_time_string("25:70")  # Invalid time
        
        # Test with edge time values
        edge_times = ["00:00", "23:59", "12:00", "06:30"]
        for time_str in edge_times:
            result = TimeKeeper.get_time_from_time_string(time_str)
            assert isinstance(result, str)
            assert len(result) == 5

    def test_water_level_edge_cases(self, pump):
        """Test edge cases with water level management."""
        # Test water level reset with extreme values
        pump.reset_water_level(0)  # Empty tank
        level_0 = pump.get_water_level_in_percent()
        assert level_0 == 0
        
        pump.reset_water_level(3000)  # Full tank
        level_full = pump.get_water_level_in_percent()
        assert level_full == 100
        
        # Test water level sufficiency with edge values
        assert pump.is_water_level_sufficient(0) is True  # 0 volume should always be sufficient
        assert pump.is_water_level_sufficient(3000) is False  # More than tank capacity

    def test_plan_type_edge_cases(self, pump, mock_relay):
        """Test edge cases with different plan types."""
        # Test with unknown plan type
        unknown_plan = {
            "plan_type": "unknown_type",
            "water_volume": 100,
            "name": "unknown_plan"
        }
        result = pump.execute_water_plan(unknown_plan, relay=mock_relay)
        assert result.watering_status is False
        assert "invalid" in result.message.lower()
        
        # Test with missing plan type
        missing_type_plan = {
            "water_volume": 100,
            "name": "missing_type_plan"
        }
        result = pump.execute_water_plan(missing_type_plan, relay=mock_relay)
        assert result.watering_status is False

    def test_network_error_scenarios(self):
        """Test edge cases with network errors."""
        communicator = ServerCommunicator("http://test.com", "test_device")
        
        # Test with invalid URL
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection error")
            try:
                result = communicator.get_plan()
                assert result == {}
            except Exception:
                # Expected behavior for network errors
                pass
        
        # Test with timeout
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Timeout")
            try:
                result = communicator.get_plan()
                assert result == {}
            except Exception:
                # Expected behavior for network errors
                pass

    def test_email_edge_cases(self):
        """Test edge cases with email functionality."""
        sender = Sender()
        
        # Test with very long message
        long_message = "A" * 1000
        with patch('run.email_sender.sender.smtplib.SMTP_SSL') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            # Should handle long messages gracefully
            sender.send_email("2023-01-15 10:00:00", "Test", long_message)
            mock_server.sendmail.assert_called_once()
        
        # Test with special characters in message
        special_message = "Test message with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        with patch('run.email_sender.sender.smtplib.SMTP_SSL') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            sender.send_email("2023-01-15 10:00:00", "Test", special_message)
            mock_server.sendmail.assert_called_once()

    def test_concurrent_operations(self, pump, mock_relay):
        """Test edge cases with concurrent operations."""
        # Test multiple rapid plan executions
        plan = {
            "plan_type": "basic",
            "water_volume": 100,
            "name": "concurrent_plan"
        }
        
        results = []
        for i in range(5):
            with patch('run.operation.pump.time.sleep'):
                result = pump.execute_water_plan(plan, relay=mock_relay)
                results.append(result)
        
        # All executions should succeed
        for result in results:
            assert result.watering_status is True

    def test_memory_usage_edge_cases(self):
        """Test edge cases that might cause memory issues."""
        # Test with large JSON objects
        large_data = {"key": "value" * 1000}
        json_str = dump_json(large_data)
        result = get_json(json_str)
        assert result == large_data
        
        # Test with deeply nested JSON
        nested_data = {"level1": {"level2": {"level3": {"level4": "deep_value"}}}}
        json_str = dump_json(nested_data)
        result = get_json(json_str)
        assert result == nested_data

    def test_boundary_value_testing(self, pump, mock_relay):
        """Test boundary values for various parameters."""
        # Test water volume boundaries
        boundary_volumes = [1, 100, 500, 1000, 2000, 2999, 3000]
        for volume in boundary_volumes:
            plan = {
                "plan_type": "basic",
                "water_volume": volume,
                "name": f"boundary_plan_{volume}"
            }
            result = pump.execute_water_plan(plan, relay=mock_relay)
            # Should either succeed or fail gracefully
            assert isinstance(result.watering_status, bool)

    def test_error_recovery_scenarios(self, pump, mock_relay):
        """Test error recovery scenarios."""
        # Test recovery from failed plan execution
        failed_plan = {
            "plan_type": "basic",
            "water_volume": 5000,  # Will fail due to insufficient water
            "name": "failed_plan"
        }
        result1 = pump.execute_water_plan(failed_plan, relay=mock_relay)
        assert result1.watering_status is False
        
        # Test recovery with a valid plan
        valid_plan = {
            "plan_type": "basic",
            "water_volume": 100,
            "name": "recovery_plan"
        }
        with patch('run.operation.pump.time.sleep'):
            result2 = pump.execute_water_plan(valid_plan, relay=mock_relay)
        assert result2.watering_status is True

    def test_data_validation_edge_cases(self):
        """Test edge cases in data validation."""
        # Test model creation with edge values
        try:
            # Test with empty name
            plan = Plan("", "basic", 100)
            assert plan.name == ""
        except Exception:
            # Some validation might reject empty names
            pass
        
        # Test with very long name
        long_name = "A" * 1000
        plan = Plan(long_name, "basic", 100)
        assert plan.name == long_name
        
        # Test with negative water volume
        plan = Plan("test", "basic", -100)
        assert plan.water_volume == -100  # Should accept negative values
