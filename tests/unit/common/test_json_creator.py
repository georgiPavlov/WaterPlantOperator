"""
Unit tests for JSON creator utilities.
"""
import pytest
import json
from run.common.json_creator import get_json, get_json_sm, dump_json


class TestJsonCreator:
    """Test cases for JSON creator functions."""

    def test_get_json_valid(self):
        """Test get_json with valid JSON string."""
        json_string = '{"name": "test", "value": 123}'
        result = get_json(json_string)
        
        expected = {"name": "test", "value": 123}
        assert result == expected

    def test_get_json_invalid(self):
        """Test get_json with invalid JSON string."""
        invalid_json = "invalid json string"
        
        # Should return empty dict instead of raising exception
        result = get_json(invalid_json)
        assert result == {}

    def test_get_json_empty(self):
        """Test get_json with empty JSON object."""
        json_string = '{}'
        result = get_json(json_string)
        
        assert result == {}

    def test_get_json_with_nested_objects(self):
        """Test get_json with nested JSON objects."""
        json_string = '{"user": {"name": "John", "age": 30}, "active": true}'
        result = get_json(json_string)
        
        expected = {"user": {"name": "John", "age": 30}, "active": True}
        assert result == expected

    def test_get_json_sm_valid(self):
        """Test get_json_sm with valid JSON string."""
        json_string = '{"name": "test", "value": 123}'
        result = get_json_sm(json_string)
        
        assert result.name == "test"
        assert result.value == 123

    def test_get_json_sm_invalid(self):
        """Test get_json_sm with invalid JSON string."""
        invalid_json = "invalid json string"
        
        # Should return None instead of raising exception
        result = get_json_sm(invalid_json)
        assert result is None

    def test_get_json_sm_with_nested_objects(self):
        """Test get_json_sm with nested JSON objects."""
        json_string = '{"user": {"name": "John", "age": 30}, "active": true}'
        result = get_json_sm(json_string)
        
        assert result.user.name == "John"
        assert result.user.age == 30
        assert result.active == True

    def test_dump_json_dict(self):
        """Test dump_json with dictionary."""
        data = {"name": "test", "value": 123}
        result = dump_json(data)
        
        expected = '{"name": "test", "value": 123}'
        assert result == expected

    def test_dump_json_list(self):
        """Test dump_json with list."""
        data = [1, 2, 3, "test"]
        result = dump_json(data)
        
        expected = '[1, 2, 3, "test"]'
        assert result == expected

    def test_dump_json_nested(self):
        """Test dump_json with nested structures."""
        data = {"users": [{"name": "John"}, {"name": "Jane"}]}
        result = dump_json(data)
        
        expected = '{"users": [{"name": "John"}, {"name": "Jane"}]}'
        assert result == expected

    def test_dump_json_with_special_characters(self):
        """Test dump_json with special characters."""
        data = {"message": "Hello, world! \"quoted\" text"}
        result = dump_json(data)
        
        expected = '{"message": "Hello, world! \\"quoted\\" text"}'
        assert result == expected

    def test_round_trip_json(self):
        """Test round trip: dump_json then get_json."""
        original_data = {"name": "test", "value": 123}
        json_string = dump_json(original_data)
        result = get_json(json_string)
        
        assert result == original_data

    def test_round_trip_json_sm(self):
        """Test round trip: dump_json then get_json_sm."""
        original_data = {"name": "test", "value": 123}
        json_string = dump_json(original_data)
        result = get_json_sm(json_string)
        
        assert result.name == original_data["name"]
        assert result.value == original_data["value"]

    def test_json_edge_cases(self):
        """Test JSON handling with edge cases."""
        # Test with very large data
        large_data = {"key": "value" * 1000}
        json_str = dump_json(large_data)
        result = get_json(json_str)
        assert result == large_data
        
        # Test with deeply nested data
        nested_data = {"level1": {"level2": {"level3": {"level4": "deep_value"}}}}
        json_str = dump_json(nested_data)
        result = get_json(json_str)
        assert result == nested_data
        
        # Test with empty strings
        empty_data = {"empty_string": "", "normal": "value"}
        json_str = dump_json(empty_data)
        result = get_json(json_str)
        assert result == empty_data
        
        # Test with None values
        none_data = {"null_value": None, "normal": "value"}
        json_str = dump_json(none_data)
        result = get_json(json_str)
        assert result == none_data

    def test_json_error_handling(self):
        """Test JSON error handling with edge cases."""
        # Test with circular reference (should fail gracefully)
        try:
            circular_data = {}
            circular_data["self"] = circular_data
            json_str = dump_json(circular_data)
            # If it doesn't raise an exception, test the result
            result = get_json(json_str)
            assert result == {}
        except (TypeError, ValueError):
            # Expected behavior for circular references
            pass
        
        # Test with non-serializable objects
        try:
            non_serializable = {"func": lambda x: x}
            json_str = dump_json(non_serializable)
            result = get_json(json_str)
            assert result == {}
        except (TypeError, ValueError):
            # Expected behavior for non-serializable objects
            pass

    def test_json_unicode_handling(self):
        """Test JSON handling with Unicode characters."""
        unicode_data = {
            "english": "Hello World",
            "chinese": "你好世界",
            "emoji": "🌱💧🌿",
            "special": "café naïve résumé"
        }
        json_str = dump_json(unicode_data)
        result = get_json(json_str)
        assert result == unicode_data
        
        # Test with SimpleNamespace
        result_sm = get_json_sm(json_str)
        assert result_sm.english == "Hello World"
        assert result_sm.chinese == "你好世界"
        assert result_sm.emoji == "🌱💧🌿"
        assert result_sm.special == "café naïve résumé"

    def test_json_new_methods(self):
        """Test new methods added to JSON creator."""
        from run.common.json_creator import is_valid_json
        
        # Test is_valid_json
        assert is_valid_json('{"key": "value"}') is True
        assert is_valid_json('invalid json') is False
        assert is_valid_json(None) is False
        assert is_valid_json("") is False
        
        # Test dump_json with indent
        data = {"name": "test", "value": 123}
        json_str_pretty = dump_json(data, indent=2)
        assert "\n" in json_str_pretty  # Should be pretty printed
        assert "  " in json_str_pretty  # Should have indentation
        
        # Test dump_json without indent
        json_str_compact = dump_json(data)
        assert "\n" not in json_str_compact  # Should be compact
