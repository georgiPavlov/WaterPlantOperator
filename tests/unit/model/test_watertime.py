"""
Unit tests for WaterTime model.
"""
import pytest
from run.model.watertime import WaterTime


class TestWaterTime:
    """Test cases for WaterTime class."""

    def test_watertime_initialization(self):
        """Test water time initialization with weekday and time."""
        weekday = "Monday"
        time_water = "08:00"
        
        water_time = WaterTime(weekday, time_water)
        
        assert water_time.weekday == weekday
        assert water_time.time_water == time_water

    def test_watertime_with_different_weekdays(self):
        """Test water time with different weekdays."""
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time_water = "10:30"
        
        for weekday in weekdays:
            water_time = WaterTime(weekday, time_water)
            assert water_time.weekday == weekday
            assert water_time.time_water == time_water

    def test_watertime_with_different_times(self):
        """Test water time with different time formats."""
        weekday = "Friday"
        times = ["00:00", "12:00", "23:59", "08:30", "15:45"]
        
        for time_water in times:
            water_time = WaterTime(weekday, time_water)
            assert water_time.weekday == weekday
            assert water_time.time_water == time_water

    def test_watertime_edge_cases(self):
        """Test water time with edge case values."""
        # Test with midnight
        water_time1 = WaterTime("Monday", "00:00")
        assert water_time1.weekday == "Monday"
        assert water_time1.time_water == "00:00"
        
        # Test with end of day
        water_time2 = WaterTime("Sunday", "23:59")
        assert water_time2.weekday == "Sunday"
        assert water_time2.time_water == "23:59"

    def test_watertime_immutability(self):
        """Test that water time attributes can be modified."""
        water_time = WaterTime("Tuesday", "14:00")
        
        # Modify attributes
        water_time.weekday = "Wednesday"
        water_time.time_water = "16:30"
        
        assert water_time.weekday == "Wednesday"
        assert water_time.time_water == "16:30"
