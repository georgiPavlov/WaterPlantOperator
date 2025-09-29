"""
Time management utilities for the water plant automation system.

This module provides time tracking and manipulation functions for
scheduling watering operations and tracking last watering times.
"""
import datetime
from typing import Optional, Union
import logging

# Constants
TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"


class TimeKeeper:
    """
    Time management class for tracking watering schedules and times.
    
    This class provides functionality to track current time, last watering time,
    and perform time-based calculations for watering schedules.
    """
    
    def __init__(self, current_time: Optional[str] = None):
        """
        Initialize TimeKeeper instance.
        
        Args:
            current_time: Initial time string in HH:MM format, defaults to current time
        """
        self.current_time = current_time or self.get_current_time()
        self.time_last_watered: Optional[str] = None
        self.date_last_watered: Optional[datetime.date] = None

    def set_current_time(self, updated_time: str) -> None:
        """
        Update the current time.
        
        Args:
            updated_time: Time string in HH:MM format
        """
        if not self._is_valid_time_format(updated_time):
            raise ValueError(f"Invalid time format: {updated_time}. Expected HH:MM")
        self.current_time = updated_time

    def set_time_last_watered(self, updated_time: str) -> None:
        """
        Set the time when the plant was last watered.
        
        Args:
            updated_time: Time string in HH:MM format
        """
        if not self._is_valid_time_format(updated_time):
            raise ValueError(f"Invalid time format: {updated_time}. Expected HH:MM")
        self.time_last_watered = updated_time

    def set_date_last_watered(self, date_last_watered: Union[datetime.date, str]) -> None:
        """
        Set the date when the plant was last watered.
        
        Args:
            date_last_watered: Date object or date string in YYYY-MM-DD format
        """
        if isinstance(date_last_watered, str):
            try:
                date_last_watered = datetime.datetime.strptime(date_last_watered, DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_last_watered}. Expected YYYY-MM-DD")
        
        if not isinstance(date_last_watered, datetime.date):
            raise TypeError("date_last_watered must be a date object or date string")
            
        self.date_last_watered = date_last_watered

    @staticmethod
    def get_current_time() -> str:
        """
        Get current time in HH:MM format.
        
        Returns:
            Current time as string in HH:MM format
        """
        now = datetime.datetime.now()
        return now.strftime(TIME_FORMAT)

    @staticmethod
    def get_current_date() -> datetime.date:
        """
        Get current date.
        
        Returns:
            Current date as date object
        """
        return datetime.date.today()

    @staticmethod
    def get_time_from_time_string(time_string: str) -> str:
        """
        Parse and format time string.
        
        Args:
            time_string: Time string in HH:MM format
            
        Returns:
            Formatted time string in HH:MM format
            
        Raises:
            ValueError: If time_string is not in valid HH:MM format
        """
        try:
            parsed_time = datetime.datetime.strptime(time_string, TIME_FORMAT)
            return parsed_time.strftime(TIME_FORMAT)
        except ValueError as e:
            raise ValueError(f"Invalid time format: {time_string}. Expected HH:MM") from e

    @staticmethod
    def get_current_time_minus_delta(delta_minutes: int) -> str:
        """
        Get current time minus specified delta in minutes.
        
        Args:
            delta_minutes: Number of minutes to subtract from current time
            
        Returns:
            Time string in HH:MM format
        """
        if not isinstance(delta_minutes, (int, float)):
            raise TypeError("delta_minutes must be a number")
            
        now = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=delta_minutes)
        time_with_delta = now - time_change
        return time_with_delta.strftime(TIME_FORMAT)

    @staticmethod
    def _is_valid_time_format(time_string: str) -> bool:
        """
        Check if time string is in valid HH:MM format.
        
        Args:
            time_string: Time string to validate
            
        Returns:
            True if valid format, False otherwise
        """
        try:
            datetime.datetime.strptime(time_string, TIME_FORMAT)
            return True
        except ValueError:
            return False

    def get_time_difference_minutes(self, time1: str, time2: str) -> int:
        """
        Calculate difference between two times in minutes.
        
        Args:
            time1: First time string in HH:MM format
            time2: Second time string in HH:MM format
            
        Returns:
            Difference in minutes (time2 - time1)
        """
        try:
            t1 = datetime.datetime.strptime(time1, TIME_FORMAT)
            t2 = datetime.datetime.strptime(time2, TIME_FORMAT)
            
            # Handle day rollover
            if t2 < t1:
                t2 += datetime.timedelta(days=1)
                
            return int((t2 - t1).total_seconds() / 60)
        except ValueError as e:
            raise ValueError(f"Invalid time format. Expected HH:MM") from e

    def is_time_within_interval(self, check_time: str, start_time: str, end_time: str) -> bool:
        """
        Check if a time falls within a given interval.
        
        Args:
            check_time: Time to check in HH:MM format
            start_time: Start of interval in HH:MM format
            end_time: End of interval in HH:MM format
            
        Returns:
            True if check_time is within interval, False otherwise
        """
        try:
            check = datetime.datetime.strptime(check_time, TIME_FORMAT)
            start = datetime.datetime.strptime(start_time, TIME_FORMAT)
            end = datetime.datetime.strptime(end_time, TIME_FORMAT)
            
            # Handle day rollover
            if end < start:
                end += datetime.timedelta(days=1)
                if check < start:
                    check += datetime.timedelta(days=1)
            
            return start <= check <= end
        except ValueError as e:
            raise ValueError(f"Invalid time format. Expected HH:MM") from e
