"""
Status model for water plant automation system.

This module defines the Status class and message constants used
for tracking watering operation results and system health.
"""
from typing import Any, Dict
from enum import Enum


class WateringStatus(Enum):
    """Enumeration for watering status values."""
    SUCCESS = True
    FAILURE = False


class Status:
    """
    Status class for tracking watering operation results.
    
    This class represents the result of a watering operation,
    including whether it was successful and any relevant messages.
    """
    
    def __init__(self, watering_status: bool, message: str):
        """
        Initialize a new Status instance.
        
        Args:
            watering_status: Boolean indicating if watering was successful
            message: Descriptive message about the operation result
        """
        if not isinstance(watering_status, bool):
            raise TypeError("watering_status must be a boolean")
        if not message or not isinstance(message, str):
            raise ValueError("message must be a non-empty string")
            
        self.watering_status = watering_status
        self.message = message

    def __repr__(self) -> str:
        """Return string representation of the status."""
        status_text = "SUCCESS" if self.watering_status else "FAILURE"
        return f'Status({status_text}, "{self.message}")'
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        status_text = "✓" if self.watering_status else "✗"
        return f"{status_text} {self.message}"
    
    def __bool__(self) -> bool:
        """Return boolean value of watering status."""
        return self.watering_status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary."""
        return {
            'watering_status': self.watering_status,
            'message': self.message
        }
    
    @classmethod
    def success(cls, message: str) -> 'Status':
        """Create a success status."""
        return cls(True, message)
    
    @classmethod
    def failure(cls, message: str) -> 'Status':
        """Create a failure status."""
        return cls(False, message)


# Message constants for consistent status messages
class StatusMessages:
    """Constants for status messages."""
    
    # Water level messages
    INSUFFICIENT_WATER = "[Insufficient water in the container]"
    SUFFICIENT_WATER = "[Sufficient water in the container]"
    
    # Success messages
    SUCCESS_MOISTURE = "[Plant successfully watered with moisture plan]"
    SUCCESS_TIMER = "[Plant successfully watered with timer plan]"
    BASIC_PLAN_SUCCESS = "[Successful watering of plant]"
    
    # Error messages
    INVALID_PLAN = "[Invalid plan]"
    DELETED_PLAN = "[Watering plan deleted]"
    PLAN_CONDITION_NOT_MET = "[Plan condition not met]"
    
    # System messages
    HEALTH_CHECK = "healthcheck"


# Backward compatibility - export constants at module level
MESSAGE_INSUFFICIENT_WATER = StatusMessages.INSUFFICIENT_WATER
MESSAGE_SUCCESS_MOISTURE = StatusMessages.SUCCESS_MOISTURE
MESSAGE_SUCCESS_TIMER = StatusMessages.SUCCESS_TIMER
MESSAGE_INVALID_PLAN = StatusMessages.INVALID_PLAN
MESSAGE_DELETED_PLAN = StatusMessages.DELETED_PLAN
MESSAGE_SUFFICIENT_WATER = StatusMessages.SUFFICIENT_WATER
MESSAGE_PLAN_CONDITION_NOT_MET = StatusMessages.PLAN_CONDITION_NOT_MET
MESSAGE_BASIC_PLAN_SUCCESS = StatusMessages.BASIC_PLAN_SUCCESS
HEALTH_CHECK = StatusMessages.HEALTH_CHECK

