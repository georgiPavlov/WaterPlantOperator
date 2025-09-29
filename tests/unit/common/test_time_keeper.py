"""
Unit tests for TimeKeeper utility.
"""
import pytest
from datetime import datetime, date, timedelta
from unittest.mock import patch
from run.common.time_keeper import TimeKeeper, TIME_FORMAT


class TestTimeKeeper:
    """Test cases for TimeKeeper class."""

    def test_time_keeper_initialization(self):
        """Test TimeKeeper initialization."""
        current_time = "10:30"
        time_keeper = TimeKeeper(current_time)
        
        assert time_keeper.current_time == current_time
        assert time_keeper.time_last_watered is None
        assert time_keeper.date_last_watered is None
        
        # Test initialization without current_time (should use current time)
        time_keeper_default = TimeKeeper()
        assert time_keeper_default.current_time is not None
        assert len(time_keeper_default.current_time) == 5  # HH:MM format

    def test_set_current_time(self):
        """Test setting current time."""
        time_keeper = TimeKeeper("10:00")
        new_time = "11:30"
        
        time_keeper.set_current_time(new_time)
        
        assert time_keeper.current_time == new_time

    def test_set_time_last_watered(self):
        """Test setting time last watered."""
        time_keeper = TimeKeeper("10:00")
        watered_time = "09:45"
        
        time_keeper.set_time_last_watered(watered_time)
        
        assert time_keeper.time_last_watered == watered_time

    def test_set_date_last_watered(self):
        """Test setting date last watered."""
        time_keeper = TimeKeeper("10:00")
        watered_date = date.today()
        
        time_keeper.set_date_last_watered(watered_date)
        
        assert time_keeper.date_last_watered == watered_date

    def test_get_current_time_static(self):
        """Test get_current_time static method."""
        result = TimeKeeper.get_current_time()
        
        # Should return a time string in HH:MM format
        assert isinstance(result, str)
        assert len(result) == 5  # HH:MM format
        assert ":" in result
        # Should be a valid time format
        parts = result.split(":")
        assert len(parts) == 2
        assert parts[0].isdigit() and parts[1].isdigit()
        assert 0 <= int(parts[0]) <= 23
        assert 0 <= int(parts[1]) <= 59

    def test_get_current_date_static(self):
        """Test get_current_date static method."""
        result = TimeKeeper.get_current_date()
        
        # Should return today's date
        assert isinstance(result, date)

    def test_get_time_from_time_string(self):
        """Test get_time_from_time_string static method."""
        time_string = "14:30"
        result = TimeKeeper.get_time_from_time_string(time_string)
        
        assert result == "14:30"

    def test_get_time_from_time_string_different_formats(self):
        """Test get_time_from_time_string with different time formats."""
        test_cases = [
            ("00:00", "00:00"),
            ("12:00", "12:00"),
            ("23:59", "23:59"),
            ("08:30", "08:30")
        ]
        
        for input_time, expected in test_cases:
            result = TimeKeeper.get_time_from_time_string(input_time)
            assert result == expected

    def test_get_time_from_time_string_invalid(self):
        """Test get_time_from_time_string with invalid format."""
        invalid_time = "25:70"  # Invalid time
        
        with pytest.raises(ValueError):
            TimeKeeper.get_time_from_time_string(invalid_time)

    def test_get_current_time_minus_delta(self):
        """Test get_current_time_minus_delta static method."""
        result = TimeKeeper.get_current_time_minus_delta(30)  # 30 minutes ago
        
        # Should return a time string in the correct format
        assert isinstance(result, str)
        assert len(result) == 5  # HH:MM format
        assert ":" in result

    def test_get_current_time_minus_delta_different_values(self):
        """Test get_current_time_minus_delta with different delta values."""
        test_cases = [0, 60, 1440]  # Different delta values
        
        for delta in test_cases:
            result = TimeKeeper.get_current_time_minus_delta(delta)
            # Should return a time string in the correct format
            assert isinstance(result, str)
            assert len(result) == 5  # HH:MM format
            assert ":" in result

    def test_time_format_constant(self):
        """Test that TIME_FORMAT constant is correct."""
        assert TIME_FORMAT == "%H:%M"

    def test_time_keeper_complete_workflow(self):
        """Test complete workflow of TimeKeeper."""
        time_keeper = TimeKeeper("10:00")
        
        # Set initial values
        time_keeper.set_time_last_watered("09:30")
        time_keeper.set_date_last_watered(date.today())
        
        # Verify values
        assert time_keeper.time_last_watered == "09:30"
        assert time_keeper.date_last_watered == date.today()
        
        # Update current time
        time_keeper.set_current_time("11:00")
        assert time_keeper.current_time == "11:00"

    def test_time_keeper_new_methods(self):
        """Test new methods added to TimeKeeper class."""
        time_keeper = TimeKeeper("10:00")
        
        # Test get_time_difference_minutes
        diff = time_keeper.get_time_difference_minutes("09:00", "10:30")
        assert diff == 90  # 1.5 hours = 90 minutes
        
        # Test day rollover
        diff_rollover = time_keeper.get_time_difference_minutes("23:00", "01:00")
        assert diff_rollover == 120  # 2 hours
        
        # Test is_time_within_interval
        assert time_keeper.is_time_within_interval("10:15", "10:00", "11:00") is True
        assert time_keeper.is_time_within_interval("09:30", "10:00", "11:00") is False
        
        # Test interval with day rollover
        assert time_keeper.is_time_within_interval("23:30", "23:00", "01:00") is True
        assert time_keeper.is_time_within_interval("22:30", "23:00", "01:00") is False

    def test_time_keeper_validation(self):
        """Test TimeKeeper validation methods."""
        time_keeper = TimeKeeper("10:00")
        
        # Test invalid time format
        with pytest.raises(ValueError):
            time_keeper.set_current_time("25:70")
        
        with pytest.raises(ValueError):
            time_keeper.set_time_last_watered("invalid")
        
        # Test invalid date format
        with pytest.raises(ValueError):
            time_keeper.set_date_last_watered("invalid-date")
        
        # Test invalid delta type
        with pytest.raises(TypeError):
            TimeKeeper.get_current_time_minus_delta("not_a_number")
        
        # Test invalid time format in difference calculation
        with pytest.raises(ValueError):
            time_keeper.get_time_difference_minutes("invalid", "10:00")
        
        # Test invalid time format in interval check
        with pytest.raises(ValueError):
            time_keeper.is_time_within_interval("invalid", "10:00", "11:00")
