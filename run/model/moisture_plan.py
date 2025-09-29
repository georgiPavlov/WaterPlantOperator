"""
MoisturePlan model for water plant automation system.

This module defines the MoisturePlan class that extends the base Plan
with moisture-specific properties like threshold and check interval.
"""
import logging
from typing import Dict, Any, Optional
import run.common.json_creator as jc
from run.model.plan import Plan


class MoisturePlan(Plan):
    """
    Moisture-based watering plan.
    
    Extends the base Plan class with moisture-specific properties
    for threshold-based watering decisions.
    
    Attributes:
        name (str): The name of the plan
        plan_type (str): The type of plan (moisture)
        water_volume (int): The amount of water to use in milliliters
        moisture_threshold (float): Moisture level threshold (0.0-1.0)
        check_interval (int): Time interval in minutes between checks
    """
    
    def __init__(self, name: str, plan_type: str, water_volume: int, 
                 moisture_threshold: float, check_interval: int):
        """
        Initialize a new MoisturePlan instance.
        
        Args:
            name: The name of the plan
            plan_type: The type of plan
            water_volume: The amount of water in milliliters
            moisture_threshold: Moisture threshold (0.0-1.0)
            check_interval: Check interval in minutes
        """
        super().__init__(name, plan_type, water_volume)
        
        if not isinstance(moisture_threshold, (int, float)) or not (0.0 <= moisture_threshold <= 1.0):
            raise ValueError("moisture_threshold must be a number between 0.0 and 1.0")
        if not isinstance(check_interval, (int, float)) or check_interval < 0:
            raise ValueError("check_interval must be a non-negative number")
            
        self.moisture_threshold = float(moisture_threshold)
        self.check_interval = int(check_interval)

    @classmethod
    def from_json(cls, json_string: str) -> Optional['MoisturePlan']:
        """
        Create a MoisturePlan instance from a JSON string.
        
        Args:
            json_string: JSON string containing plan data
            
        Returns:
            MoisturePlan instance or None if parsing fails
        """
        try:
            json_dict = jc.get_json(json_string)
            if not json_dict:
                return None
                
            # Validate required fields
            required_fields = ['name', 'plan_type', 'water_volume', 'moisture_threshold', 'check_interval']
            for field in required_fields:
                if field not in json_dict:
                    raise TypeError(f"Missing required field: {field}")
            
            # Only pass required fields to constructor
            plan_data = {field: json_dict[field] for field in required_fields}
            return cls(**plan_data)
        except Exception as e:
            logging.error(f"Failed to create MoisturePlan from JSON: {e}")
            return None

    def __repr__(self) -> str:
        """Return string representation of the moisture plan."""
        return (f'MoisturePlan(name="{self.name}", type="{self.plan_type}", '
                f'volume={self.water_volume}ml, threshold={self.moisture_threshold}, '
                f'interval={self.check_interval}min)')
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        return (f"{self.name} (moisture): {self.water_volume}ml, "
                f"threshold={self.moisture_threshold}, interval={self.check_interval}min")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert moisture plan to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            'moisture_threshold': self.moisture_threshold,
            'check_interval': self.check_interval
        })
        return base_dict
