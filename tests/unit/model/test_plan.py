"""
Unit tests for Plan model.
"""
import pytest
import json
from run.model.plan import Plan


class TestPlan:
    """Test cases for Plan class."""

    def test_plan_initialization(self):
        """Test plan initialization with all parameters."""
        name = "test_plan"
        plan_type = "basic"
        water_volume = 200
        
        plan = Plan(name, plan_type, water_volume)
        
        assert plan.name == name
        assert plan.plan_type == plan_type
        assert plan.water_volume == water_volume

    def test_plan_from_json(self):
        """Test creating plan from JSON string."""
        json_string = '{"name": "plant1", "plan_type": "basic", "water_volume": 200}'
        
        plan = Plan.from_json(json_string)
        
        assert plan.name == "plant1"
        assert plan.plan_type == "basic"
        assert plan.water_volume == 200

    def test_plan_from_json_invalid(self):
        """Test creating plan from invalid JSON."""
        invalid_json = "invalid json string"
        
        # Should return None instead of raising exception
        result = Plan.from_json(invalid_json)
        assert result is None

    def test_plan_repr(self):
        """Test plan string representation."""
        name = "test_plan"
        plan = Plan(name, "basic", 200)
        
        expected_repr = f'Plan(name="{name}", type="basic", volume=200ml)'
        assert repr(plan) == expected_repr

    def test_plan_from_json_missing_fields(self):
        """Test creating plan from JSON missing required fields."""
        json_string = json.dumps({"name": "test"})  # Missing plan_type and water_volume
        
        # Should return None instead of raising exception
        result = Plan.from_json(json_string)
        assert result is None

    def test_plan_with_different_types(self):
        """Test plan with different data types."""
        name = "numeric_plan"
        plan_type = "advanced"
        water_volume = 500  # Numeric instead of string
        
        plan = Plan(name, plan_type, water_volume)
        
        assert plan.name == name
        assert plan.plan_type == plan_type
        assert plan.water_volume == water_volume

    def test_plan_edge_cases(self):
        """Test plan with edge case values."""
        # Test with empty name (should raise ValueError)
        with pytest.raises(ValueError):
            Plan("", "basic", 100)
        
        # Test with very long name
        long_name = "A" * 1000
        plan = Plan(long_name, "basic", 100)
        assert plan.name == long_name
        
        # Test with negative water volume (should raise ValueError)
        with pytest.raises(ValueError):
            Plan("test", "basic", -100)
        
        # Test with zero water volume
        plan = Plan("test", "basic", 0)
        assert plan.water_volume == 0
        
        # Test with very large water volume
        plan = Plan("test", "basic", 1000000)
        assert plan.water_volume == 1000000
        
        # Test with float water volume (should be converted to int)
        plan = Plan("test", "basic", 100.5)
        assert plan.water_volume == 100

    def test_plan_from_json_edge_cases(self):
        """Test plan from_json with edge cases."""
        # Test with missing required fields
        incomplete_json = '{"name": "test"}'
        result = Plan.from_json(incomplete_json)
        assert result is None
        
        # Test with extra fields (should work with new implementation)
        extra_json = '{"name": "test", "plan_type": "basic", "water_volume": 100, "extra_field": "value"}'
        result = Plan.from_json(extra_json)
        assert result is not None
        assert result.name == "test"
        assert result.plan_type == "basic"
        assert result.water_volume == 100
        
        # Test with null values
        null_json = '{"name": null, "plan_type": "basic", "water_volume": 100}'
        result = Plan.from_json(null_json)
        assert result is None

    def test_plan_new_methods(self):
        """Test new methods added to Plan class."""
        plan = Plan("test_plan", "basic", 200)
        
        # Test __str__ method
        str_repr = str(plan)
        assert "test_plan" in str_repr
        assert "basic" in str_repr
        assert "200ml" in str_repr
        
        # Test to_dict method
        plan_dict = plan.to_dict()
        assert plan_dict == {
            'name': 'test_plan',
            'plan_type': 'basic',
            'water_volume': 200
        }
        
        # Test __repr__ method
        repr_str = repr(plan)
        assert 'Plan(' in repr_str
        assert 'test_plan' in repr_str
        assert 'basic' in repr_str
        assert '200ml' in repr_str
