"""
Plan model for water plant automation system.

This module defines the base Plan class that represents a watering plan
with basic properties like name, type, and water volume.
"""
import logging
from typing import Dict, Any, Optional
import run.common.json_creator as jc


class Plan:
    """
    Base class for watering plans.
    
    Attributes:
        name (str): The name of the plan
        plan_type (str): The type of plan (basic, moisture, time_based)
        water_volume (int): The amount of water to use in milliliters
    """
    
    def __init__(self, name: str, plan_type: str, water_volume: int):
        """
        Initialize a new Plan instance.
        
        Args:
            name: The name of the plan
            plan_type: The type of plan
            water_volume: The amount of water in milliliters
        """
        if not name or not isinstance(name, str):
            raise ValueError("Plan name must be a non-empty string")
        if not plan_type or not isinstance(plan_type, str):
            raise ValueError("Plan type must be a non-empty string")
        if not isinstance(water_volume, (int, float)) or water_volume < 0:
            raise ValueError("Water volume must be a non-negative number")
            
        self.name = name
        self.plan_type = plan_type
        self.water_volume = int(water_volume)

    @classmethod
    def from_json(cls, json_string: str) -> Optional['Plan']:
        """
        Create a Plan instance from a JSON string.
        
        Args:
            json_string: JSON string containing plan data
            
        Returns:
            Plan instance or None if parsing fails
            
        Raises:
            TypeError: If required fields are missing
        """
        try:
            json_dict = jc.get_json(json_string)
            if not json_dict:
                return None
                
            # Validate required fields
            required_fields = ['name', 'plan_type', 'water_volume']
            for field in required_fields:
                if field not in json_dict:
                    raise TypeError(f"Missing required field: {field}")
            
            # Only pass required fields to constructor
            plan_data = {field: json_dict[field] for field in required_fields}
            return cls(**plan_data)
        except Exception as e:
            logging.error(f"Failed to create Plan from JSON: {e}")
            return None

    def __repr__(self) -> str:
        """Return string representation of the plan."""
        return f'Plan(name="{self.name}", type="{self.plan_type}", volume={self.water_volume}ml)'
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        return f"{self.name} ({self.plan_type}): {self.water_volume}ml"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary."""
        return {
            'name': self.name,
            'plan_type': self.plan_type,
            'water_volume': self.water_volume
        }