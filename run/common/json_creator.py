"""
JSON utility functions for the water plant automation system.

This module provides safe JSON parsing and serialization functions
with proper error handling and logging.
"""
import json
import logging
from typing import Any, Dict, Optional, Union
from types import SimpleNamespace


def get_json(json_string: Union[str, None]) -> Dict[str, Any]:
    """
    Safely parse JSON string to dictionary.
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        Dictionary representation of JSON, or empty dict if parsing fails
    """
    if not json_string:
        logging.warning("Empty or None JSON string provided")
        return {}
        
    try:
        logging.debug(f'Parsing JSON: {json_string[:100]}...' if len(json_string) > 100 else f'Parsing JSON: {json_string}')
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error parsing JSON: {e}")
        return {}


def get_json_sm(json_string: Union[str, None]) -> Optional[SimpleNamespace]:
    """
    Safely parse JSON string to SimpleNamespace object.
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        SimpleNamespace object or None if parsing fails
    """
    if not json_string:
        logging.warning("Empty or None JSON string provided")
        return None
        
    try:
        logging.debug(f'Parsing JSON to SimpleNamespace: {json_string[:100]}...' if len(json_string) > 100 else f'Parsing JSON: {json_string}')
        return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error parsing JSON: {e}")
        return None


def dump_json(data: Any, indent: Optional[int] = None) -> str:
    """
    Safely serialize data to JSON string.
    
    Args:
        data: Data to serialize
        indent: Optional indentation for pretty printing
        
    Returns:
        JSON string representation of data
        
    Raises:
        TypeError: If data is not JSON serializable
    """
    try:
        logging.debug(f'Serializing data to JSON: {type(data).__name__}')
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except TypeError as e:
        logging.error(f"Data not JSON serializable: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error serializing JSON: {e}")
        raise


def is_valid_json(json_string: Union[str, None]) -> bool:
    """
    Check if a string is valid JSON.
    
    Args:
        json_string: String to validate
        
    Returns:
        True if valid JSON, False otherwise
    """
    if not json_string:
        return False
        
    try:
        json.loads(json_string)
        return True
    except (json.JSONDecodeError, TypeError):
        return False
