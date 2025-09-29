"""
Unit tests for TimePlan model.
"""
import pytest
import json
from run.model.time_plan import TimePlan
from run.model.watertime import WaterTime


class TestTimePlan:
    """Test cases for TimePlan class."""

    def test_time_plan_initialization(self):
        """Test time plan initialization with all parameters."""
        name = "time_plan"
        plan_type = "time_based"
        water_volume = 200
        weekday_times = [
            WaterTime("Monday", "08:00"),
            WaterTime("Friday", "18:00")
        ]
        execute_only_once = False
        
        plan = TimePlan(name, plan_type, water_volume, weekday_times, execute_only_once)
        
        assert plan.name == name
        assert plan.plan_type == plan_type
        assert plan.water_volume == water_volume
        assert plan.weekday_times == weekday_times
        assert plan.execute_only_once == execute_only_once

    def test_time_plan_inheritance(self):
        """Test that TimePlan inherits from Plan."""
        weekday_times = [WaterTime("Monday", "08:00")]
        plan = TimePlan("test", "time_based", 200, weekday_times, False)
        
        # Check that it has Plan attributes
        assert hasattr(plan, 'name')
        assert hasattr(plan, 'plan_type')
        assert hasattr(plan, 'water_volume')
        
        # Check that it has TimePlan specific attributes
        assert hasattr(plan, 'weekday_times')
        assert hasattr(plan, 'execute_only_once')

    def test_time_plan_from_json(self):
        """Test creating time plan from JSON string."""
        json_string = json.dumps({
            "name": "time_plan",
            "plan_type": "time_based",
            "water_volume": 150,
            "weekday_times": [
                {"weekday": "Monday", "time_water": "08:00"},
                {"weekday": "Friday", "time_water": "18:00"}
            ],
            "execute_only_once": True
        })
        
        plan = TimePlan.from_json(json_string)
        
        assert plan.name == "time_plan"
        assert plan.plan_type == "time_based"
        assert plan.water_volume == 150
        assert plan.execute_only_once == True
        assert len(plan.weekday_times) == 2
        assert plan.weekday_times[0].weekday == "Monday"
        assert plan.weekday_times[0].time_water == "08:00"
        assert plan.weekday_times[1].weekday == "Friday"
        assert plan.weekday_times[1].time_water == "18:00"

    def test_time_plan_from_json_invalid(self):
        """Test creating time plan from invalid JSON."""
        invalid_json = "invalid json string"
        
        # Should return None instead of raising exception
        result = TimePlan.from_json(invalid_json)
        assert result is None

    def test_time_plan_repr(self):
        """Test time plan string representation."""
        name = "test_time_plan"
        weekday_times = [WaterTime("Monday", "08:00")]
        plan = TimePlan(name, "time_based", 200, weekday_times, False)
        
        expected_repr = f'TimePlan(name="{name}", type="time_based", volume=200ml, times=1, once=False)'
        assert repr(plan) == expected_repr

    def test_time_plan_with_empty_weekday_times(self):
        """Test time plan with empty weekday times list."""
        plan = TimePlan("empty_plan", "time_based", 100, [], True)
        
        assert plan.weekday_times == []
        assert plan.execute_only_once == True

    def test_time_plan_with_single_weekday_time(self):
        """Test time plan with single weekday time."""
        weekday_times = [WaterTime("Wednesday", "12:00")]
        plan = TimePlan("single_plan", "time_based", 300, weekday_times, False)
        
        assert len(plan.weekday_times) == 1
        assert plan.weekday_times[0].weekday == "Wednesday"
        assert plan.weekday_times[0].time_water == "12:00"
