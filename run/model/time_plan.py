"""
TimePlan model for water plant automation system.

This module defines the TimePlan class that extends the base Plan
with time-based scheduling properties for scheduled watering.
"""
import logging
from typing import List, Dict, Any, Optional
import run.common.json_creator as jc
from run.model.plan import Plan
from run.model.watertime import WaterTime


class TimePlan(Plan):
    """
    Time-based watering plan.
    
    Extends the base Plan class with time-based scheduling properties
    for scheduled watering at specific times and days.
    
    Attributes:
        name (str): The name of the plan
        plan_type (str): The type of plan (time_based)
        water_volume (int): The amount of water to use in milliliters
        weekday_times (List[WaterTime]): List of scheduled watering times
        execute_only_once (bool): Whether to execute only once per day
    """
    
    def __init__(self, name: str, plan_type: str, water_volume: int, 
                 weekday_times: List[WaterTime], execute_only_once: bool = False) -> None:
        """
        Initialize a new TimePlan instance.
        
        Args:
            name: The name of the plan
            plan_type: The type of plan
            water_volume: The amount of water in milliliters
            weekday_times: List of scheduled watering times
            execute_only_once: Whether to execute only once per day
        """
        super().__init__(name, plan_type, water_volume)
        
        if not isinstance(weekday_times, list):
            raise TypeError("weekday_times must be a list")
        if not all(isinstance(wt, WaterTime) for wt in weekday_times):
            raise TypeError("All weekday_times must be WaterTime instances")
        if not isinstance(execute_only_once, bool):
            raise TypeError("execute_only_once must be a boolean")
            
        self.weekday_times = weekday_times
        self.execute_only_once = execute_only_once

    @classmethod
    def from_json(cls, json_string: str) -> Optional['TimePlan']:
        """
        Create a TimePlan instance from a JSON string.
        
        Args:
            json_string: JSON string containing plan data
            
        Returns:
            TimePlan instance or None if parsing fails
        """
        try:
            time_plan = jc.get_json_sm(json_string)
            if not time_plan:
                return None
                
            # Validate required fields
            required_fields = ['name', 'plan_type', 'water_volume', 'weekday_times']
            for field in required_fields:
                if not hasattr(time_plan, field):
                    raise TypeError(f"Missing required field: {field}")
            
            # Convert weekday_times to WaterTime objects
            weekday_times = []
            for wt_data in time_plan.weekday_times:
                if hasattr(wt_data, 'weekday') and hasattr(wt_data, 'time_water'):
                    water_time = WaterTime(wt_data.weekday, wt_data.time_water)
                    weekday_times.append(water_time)
                else:
                    raise ValueError("Invalid weekday_times format")
            
            execute_only_once = getattr(time_plan, 'execute_only_once', False)
            
            return cls(time_plan.name, time_plan.plan_type, time_plan.water_volume, 
                      weekday_times, execute_only_once)
        except Exception as e:
            logging.error(f"Failed to create TimePlan from JSON: {e}")
            return None

    def __repr__(self) -> str:
        """Return string representation of the time plan."""
        return (f'TimePlan(name="{self.name}", type="{self.plan_type}", '
                f'volume={self.water_volume}ml, times={len(self.weekday_times)}, '
                f'once={self.execute_only_once})')
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        times_str = ", ".join([f"{wt.weekday} {wt.time_water}" for wt in self.weekday_times])
        return f"{self.name} (time): {self.water_volume}ml, times=[{times_str}], once={self.execute_only_once}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert time plan to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            'weekday_times': [{'weekday': wt.weekday, 'time_water': wt.time_water} for wt in self.weekday_times],
            'execute_only_once': self.execute_only_once
        })
        return base_dict

