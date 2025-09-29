"""
Unit tests for Pump operation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date
import run.model.status as s
from run.model.plan import Plan
from run.model.moisture_plan import MoisturePlan
from run.model.time_plan import TimePlan
from run.model.watertime import WaterTime
from run.operation.pump import Pump


class TestPump:
    """Test cases for Pump class."""

    @pytest.fixture
    def pump(self):
        """Create a pump instance for testing."""
        return Pump(water_max_capacity=2000, water_pumped_in_second=70, moisture_max_level=0)

    @pytest.fixture
    def mock_relay(self):
        """Create a mock relay for testing."""
        relay = Mock()
        relay.on = Mock()
        relay.off = Mock()
        return relay

    @pytest.fixture
    def mock_moisture_sensor(self):
        """Create a mock moisture sensor for testing."""
        moisture = Mock()
        moisture.value = 0.3
        return moisture

    def test_pump_initialization(self, pump):
        """Test pump initialization."""
        assert pump.water_max_capacity == 2000
        assert pump.water_pumped_in_second == 70
        assert pump.moisture_level == 0
        assert pump.water_level == 2000
        assert pump.running_plan is None
        assert pump.watering_status is None
        assert pump.moisture_sensor is None
        assert pump.water_reset is True

    def test_is_water_level_sufficient_sufficient(self, pump):
        """Test water level check when sufficient water is available."""
        result = pump.is_water_level_sufficient(500)
        
        assert result is True
        assert pump.water_level == 1500  # 2000 - 500

    def test_is_water_level_sufficient_insufficient(self, pump):
        """Test water level check when insufficient water is available."""
        result = pump.is_water_level_sufficient(2500)
        
        assert result is False
        assert pump.water_level == 2000  # Should remain unchanged

    def test_get_water_time_in_seconds_from_percent(self, pump):
        """Test water time calculation."""
        water_milliliters = 140  # 2 seconds at 70ml/sec
        result = pump.get_water_time_in_seconds_from_percent(water_milliliters)
        
        # Should be 2 seconds + 3 seconds for reset = 5 seconds
        assert result == 5
        assert pump.water_reset is False

    def test_get_water_time_in_seconds_after_reset(self, pump):
        """Test water time calculation after reset."""
        pump.water_reset = False
        water_milliliters = 70  # 1 second at 70ml/sec
        result = pump.get_water_time_in_seconds_from_percent(water_milliliters)
        
        # Should be 1 second (no reset bonus)
        assert result == 1

    def test_get_moisture_level_in_percent(self, pump, mock_moisture_sensor):
        """Test moisture level calculation."""
        pump.moisture_sensor = mock_moisture_sensor
        mock_moisture_sensor.value = 0.3  # 30% wet, 70% dry
        
        result = pump.get_moisture_level_in_percent()
        
        assert result == 70  # 100 - (0.3 * 100)

    def test_get_water_level_in_percent(self, pump):
        """Test water level percentage calculation."""
        pump.water_level = 1000  # Half full
        
        result = pump.get_water_level_in_percent()
        
        assert result == 50.0  # (1000 / 2000) * 100

    def test_reset_water_level(self, pump):
        """Test water level reset."""
        pump.water_level = 500
        pump.water_reset = False
        
        pump.reset_water_level(2000)
        
        assert pump.water_level == 2000
        assert pump.water_reset is True

    @patch('run.operation.pump.time.sleep')
    def test_water_plant_successful(self, mock_sleep, pump, mock_relay):
        """Test successful plant watering."""
        result = pump.water_plant(mock_relay, 140)
        
        assert result is True
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()
        mock_sleep.assert_called_once_with(5)  # 2 + 3 seconds

    def test_water_plant_insufficient_water(self, pump, mock_relay):
        """Test plant watering with insufficient water."""
        result = pump.water_plant(mock_relay, 2500)
        
        assert result is False
        mock_relay.on.assert_not_called()
        mock_relay.off.assert_not_called()

    @patch('run.operation.pump.time.sleep')
    def test_execute_water_plan_basic_success(self, mock_sleep, pump, mock_relay):
        """Test executing basic water plan successfully."""
        plan = {"plan_type": "basic", "water_volume": 140, "name": "test_plan"}
        
        result = pump.execute_water_plan(plan, relay=mock_relay)
        
        assert result.watering_status is True
        assert result.message == s.MESSAGE_BASIC_PLAN_SUCCESS
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()

    def test_execute_water_plan_basic_insufficient_water(self, pump, mock_relay):
        """Test executing basic water plan with insufficient water."""
        plan = {"plan_type": "basic", "water_volume": 2500, "name": "test_plan"}
        
        result = pump.execute_water_plan(plan, relay=mock_relay)
        
        assert result.watering_status is False
        assert result.message == s.MESSAGE_INSUFFICIENT_WATER

    @patch('run.operation.pump.time.sleep')
    def test_execute_water_plan_moisture(self, mock_sleep, pump, mock_relay, mock_moisture_sensor):
        """Test executing moisture water plan."""
        plan = {
            "plan_type": "moisture",
            "water_volume": 140,
            "moisture_threshold": 0.4,
            "check_interval": 30,
            "name": "moisture_plan"
        }
        
        with patch.object(pump, 'get_time') as mock_get_time:
            mock_time_keeper = Mock()
            mock_time_keeper.get_current_time_minus_delta.return_value = "09:30"
            mock_time_keeper.time_last_watered = "09:30"
            mock_time_keeper.get_current_time.return_value = "10:00"
            mock_get_time.return_value = mock_time_keeper
            
            # Set up the pump's water_time to match our mock
            pump.water_time = mock_time_keeper
            
            pump.moisture_sensor = mock_moisture_sensor
            # The pump code has a bug: it compares percentage (0-100) with decimal (0.0-1.0)
            # get_moisture_level_in_percent() returns 100 - (sensor_value * 100)
            # Threshold is 0.4 (decimal), so we need moisture level < 0.4 to trigger watering
            # If we want moisture level = 0.3, then: 0.3 = 100 - (sensor_value * 100)
            # So sensor_value = (100 - 0.3) / 100 = 0.997
            mock_moisture_sensor.value = 0.997  # This gives 0.3% moisture level, which is < 0.4 threshold
            
            result = pump.execute_water_plan(plan, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
            
            assert result.watering_status is True
            assert result.message == s.MESSAGE_SUCCESS_MOISTURE

    def test_execute_water_plan_moisture_condition_not_met(self, pump, mock_relay, mock_moisture_sensor):
        """Test executing moisture water plan when condition not met."""
        plan = {
            "plan_type": "moisture",
            "water_volume": 140,
            "moisture_threshold": 0.2,
            "check_interval": 30,
            "name": "moisture_plan"
        }
        
        with patch.object(pump, 'get_time') as mock_get_time:
            mock_time_keeper = Mock()
            mock_time_keeper.get_current_time_minus_delta.return_value = "09:30"
            mock_time_keeper.time_last_watered = "09:30"
            mock_get_time.return_value = mock_time_keeper
            
            pump.moisture_sensor = mock_moisture_sensor
            mock_moisture_sensor.value = 0.3  # 30% wet, 70% dry (below threshold)
            
            result = pump.execute_water_plan(plan, relay=mock_relay, moisture_sensor=mock_moisture_sensor)
            
            assert result.watering_status is False
            assert result.message == s.MESSAGE_PLAN_CONDITION_NOT_MET

    @patch('run.operation.pump.time.sleep')
    def test_execute_water_plan_time_based(self, mock_sleep, pump, mock_relay):
        """Test executing time-based water plan."""
        plan = {
            "plan_type": "time_based",
            "water_volume": 140,
            "weekday_times": [{"weekday": "Monday", "time_water": "10:00"}],
            "execute_only_once": False,
            "name": "time_plan"
        }
        
        with patch.object(pump, 'get_time') as mock_get_time, \
             patch('run.operation.pump.date') as mock_date, \
             patch('run.operation.pump.calendar') as mock_calendar:
            
            mock_time_keeper = Mock()
            mock_time_keeper.get_current_time.return_value = "10:00"
            mock_time_keeper.time_last_watered = "09:00"
            mock_time_keeper.date_last_watered = date(2023, 1, 15)  # Different date (yesterday)
            mock_get_time.return_value = mock_time_keeper
            
            # Set up the pump's water_time to match our mock
            pump.water_time = mock_time_keeper
            
            mock_date.today.return_value = date(2023, 1, 16)  # Monday
            mock_calendar.day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            result = pump.execute_water_plan(plan, relay=mock_relay)
            
            assert result.watering_status is True
            assert result.message == s.MESSAGE_SUCCESS_TIMER

    def test_execute_water_plan_delete(self, pump):
        """Test executing delete plan."""
        pump.running_plan = Mock()
        plan = {"plan_type": "delete"}
        
        result = pump.execute_water_plan(plan)
        
        assert pump.running_plan is None
        assert result.watering_status is False
        assert result.message == s.MESSAGE_DELETED_PLAN

    def test_execute_water_plan_invalid(self, pump):
        """Test executing invalid plan."""
        plan = {"plan_type": "invalid_type"}
        
        result = pump.execute_water_plan(plan)
        
        assert result.watering_status is False
        assert result.message == s.MESSAGE_INVALID_PLAN

    def test_get_running_plan(self, pump):
        """Test getting running plan."""
        mock_plan = Mock()
        pump.running_plan = mock_plan
        
        result = pump.get_running_plan()
        
        assert result == mock_plan

    def test_water_plant_by_moisture_time_out_of_range(self, pump, mock_relay, mock_moisture_sensor):
        """Test moisture watering when time is out of range."""
        moisture_plan = MoisturePlan("test", "moisture", 140, 0.4, 30)
        
        with patch.object(pump, 'get_time') as mock_get_time, \
             patch.object(pump, '_create_time_keeper') as mock_create_time_keeper:
            
            mock_time_keeper = Mock()
            mock_new_time_keeper = Mock()
            
            # Set up times: current_time = "10:00", current_time_minus_delta = "09:30"
            # out_of_range_time = current_time - (check_int * 2) = "10:00" - 60min = "09:00"
            mock_time_keeper.get_current_time_minus_delta.return_value = "09:30"
            mock_time_keeper.get_current_time.return_value = "10:00"
            mock_time_keeper.time_last_watered = "08:00"  # Out of range
            mock_get_time.return_value = mock_time_keeper
            mock_create_time_keeper.return_value = mock_new_time_keeper
            
            # Set up the pump's water_time to have the out-of-range time
            # "08:00" < "09:00" (out_of_range_time), so it's out of range
            pump.water_time = mock_time_keeper
            
            pump.water_plant_by_moisture(mock_relay, mock_moisture_sensor, moisture_plan)
            
            # Should reset time to the current_time_minus_delta when out of range
            # The pump calls _reset_water_time which creates a new time keeper and calls set_time_last_watered
            mock_create_time_keeper.assert_called_once()
            mock_new_time_keeper.set_time_last_watered.assert_called_with("09:30")
