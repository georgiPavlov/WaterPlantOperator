"""
Unit tests for MoisturePlan model.
"""
import pytest
import json
from run.model.moisture_plan import MoisturePlan


class TestMoisturePlan:
    """Test cases for MoisturePlan class."""

    def test_moisture_plan_initialization(self):
        """Test moisture plan initialization with all parameters."""
        name = "moisture_plan"
        plan_type = "moisture"
        water_volume = 200
        moisture_threshold = 0.4
        check_interval = 30
        
        plan = MoisturePlan(name, plan_type, water_volume, moisture_threshold, check_interval)
        
        assert plan.name == name
        assert plan.plan_type == plan_type
        assert plan.water_volume == water_volume
        assert plan.moisture_threshold == moisture_threshold
        assert plan.check_interval == check_interval

    def test_moisture_plan_inheritance(self):
        """Test that MoisturePlan inherits from Plan."""
        plan = MoisturePlan("test", "moisture", 200, 0.5, 60)
        
        # Check that it has Plan attributes
        assert hasattr(plan, 'name')
        assert hasattr(plan, 'plan_type')
        assert hasattr(plan, 'water_volume')
        
        # Check that it has MoisturePlan specific attributes
        assert hasattr(plan, 'moisture_threshold')
        assert hasattr(plan, 'check_interval')

    def test_moisture_plan_from_json(self):
        """Test creating moisture plan from JSON string."""
        json_string = json.dumps({
            "name": "moisture_plan",
            "plan_type": "moisture",
            "water_volume": 150,
            "moisture_threshold": 0.3,
            "check_interval": 45
        })
        
        plan = MoisturePlan.from_json(json_string)
        
        assert plan.name == "moisture_plan"
        assert plan.plan_type == "moisture"
        assert plan.water_volume == 150
        assert plan.moisture_threshold == 0.3
        assert plan.check_interval == 45

    def test_moisture_plan_from_json_invalid(self):
        """Test creating moisture plan from invalid JSON."""
        invalid_json = "invalid json string"
        
        # Should return None instead of raising exception
        result = MoisturePlan.from_json(invalid_json)
        assert result is None

    def test_moisture_plan_repr(self):
        """Test moisture plan string representation."""
        name = "test_moisture_plan"
        plan = MoisturePlan(name, "moisture", 200, 0.4, 30)
        
        expected_repr = f'MoisturePlan(name="{name}", type="moisture", volume=200ml, threshold=0.4, interval=30min)'
        assert repr(plan) == expected_repr

    def test_moisture_plan_with_edge_values(self):
        """Test moisture plan with edge case values."""
        # Test with minimum threshold
        plan1 = MoisturePlan("min_plan", "moisture", 100, 0.0, 1)
        assert plan1.moisture_threshold == 0.0
        assert plan1.check_interval == 1
        
        # Test with maximum threshold
        plan2 = MoisturePlan("max_plan", "moisture", 1000, 1.0, 1440)  # 24 hours
        assert plan2.moisture_threshold == 1.0
        assert plan2.check_interval == 1440
