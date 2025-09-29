"""
Pump operation module for water plant automation system.

This module provides the core watering functionality including basic watering,
moisture-based watering, and time-based watering with comprehensive logging
and status tracking.
"""
import time
import logging
from datetime import date
import calendar
from typing import Dict, Any, Optional, Union
from run.common import time_keeper as tk
import run.model.status as s
import run.model.plan as p
import run.model.moisture_plan as m
import run.model.time_plan as t
import run.common.json_creator as j


class IPumpInterface:
    """Interface defining the contract for pump operations."""

    def execute_water_plan(self, plan: Union[Dict[str, Any], p.Plan], **sensors) -> s.Status:
        """Execute a watering plan based on plan type."""
        pass

    def is_water_level_sufficient(self, water_milliliters: int) -> bool:
        """Check if there's sufficient water for the requested amount."""
        pass

    def water_plant(self, relay, water_milliliters: int) -> bool:
        """Execute the actual watering operation."""
        pass

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan: m.MoisturePlan) -> None:
        """Water plant based on moisture sensor readings."""
        pass

    def water_plant_by_timer(self, relay, time_plan: t.TimePlan) -> None:
        """Water plant based on scheduled times."""
        pass

    def get_water_time_in_seconds_from_percent(self, water_milliliters: int) -> int:
        """Calculate watering duration in seconds based on water volume."""
        pass

    def get_moisture_level_in_percent(self) -> int:
        """Get current moisture level as percentage."""
        pass

    def get_water_level_in_percent(self) -> float:
        """Get current water level as percentage of capacity."""
        pass


class Pump(IPumpInterface):
    """
    Main pump class for water plant automation.
    
    Handles all watering operations including basic, moisture-based, and time-based
    watering with comprehensive status tracking and logging.
    """
    
    # Plan type constants
    WATER_PLAN_BASIC = 'basic'
    WATER_PLAN_TIME = 'time_based'
    WATER_PLAN_MOISTURE = 'moisture'
    DELETE_RUNNING_PLAN = 'delete'
    
    # Sensor key constants
    RELAY_SENSOR_KEY = 'relay'
    MOISTURE_SENSOR_KEY = 'moisture_sensor'
    PLAN_TYPE_KEY = 'plan_type'

    def __init__(self, water_max_capacity: int, water_pumped_in_second: int, moisture_max_level: int):
        """
        Initialize the pump with capacity and performance parameters.
        
        Args:
            water_max_capacity: Maximum water capacity in milliliters
            water_pumped_in_second: Water pumping rate in ml/second
            moisture_max_level: Maximum moisture level for sensor calibration
        """
        super().__init__()
        
        # Initialize time tracking
        self._initialize_time_tracking()
        
        # Set capacity and performance parameters
        self.water_max_capacity = water_max_capacity
        self.water_level = self.water_max_capacity
        self.water_pumped_in_second = water_pumped_in_second
        self.moisture_max_level = moisture_max_level
        
        # Initialize state variables
        self.moisture_level = moisture_max_level
        self.running_plan: Optional[Union[p.Plan, m.MoisturePlan, t.TimePlan]] = None
        self.watering_status: Optional[s.Status] = None
        self.moisture_sensor = None
        self.water_reset = True
        
        logging.info(f"Pump initialized: capacity={water_max_capacity}ml, rate={water_pumped_in_second}ml/s")

    def _initialize_time_tracking(self) -> None:
        """Initialize time tracking for watering operations."""
        self.water_time = self._create_time_keeper()
        self.water_time.set_date_last_watered(self.water_time.get_current_date())
        self.water_time.set_time_last_watered(self.water_time.get_current_time())
        logging.info("Time tracking initialized")

    def _create_time_keeper(self) -> tk.TimeKeeper:
        """Create a new time keeper instance."""
        return tk.TimeKeeper(tk.TimeKeeper.get_current_time())

    def execute_water_plan(self, plan: Union[Dict[str, Any], p.Plan], **sensors) -> s.Status:
        """
        Execute a watering plan based on its type.
        
        Args:
            plan: Watering plan (dict or Plan object)
            **sensors: Sensor objects (relay, moisture_sensor, etc.)
            
        Returns:
            Status object indicating success or failure
        """
        logging.info(f"Executing plan: {plan}")
        
        # Extract plan type and relay
        plan_type = self._extract_plan_type(plan)
        relay = sensors.get(self.RELAY_SENSOR_KEY)
        
        logging.info(f"Plan type: {plan_type}")
        
        # Route to appropriate handler based on plan type
        if plan_type == self.WATER_PLAN_BASIC:
            self._execute_basic_plan(plan, relay)
        elif plan_type == self.WATER_PLAN_MOISTURE:
            self._execute_moisture_plan(plan, relay, sensors)
        elif plan_type == self.WATER_PLAN_TIME:
            self._execute_time_plan(plan, relay)
        elif plan_type == self.DELETE_RUNNING_PLAN:
            self._delete_running_plan()
        else:
            self._handle_invalid_plan(plan_type)
            
        return self.watering_status

    def _extract_plan_type(self, plan: Union[Dict[str, Any], p.Plan]) -> str:
        """Extract plan type from plan object or dictionary."""
        if isinstance(plan, dict):
            return plan[self.PLAN_TYPE_KEY]
        return plan.plan_type

    def _execute_basic_plan(self, plan: Union[Dict[str, Any], p.Plan], relay) -> None:
        """Execute a basic watering plan."""
        logging.info(f"Executing basic plan: {self.WATER_PLAN_BASIC}")
        
        # Convert dict to Plan object if needed
        if isinstance(plan, dict):
            json_string = j.dump_json(plan)
            logging.info(f"Plan JSON: {json_string}")
            plan_obj = p.Plan.from_json(json_string)
        else:
            plan_obj = plan
            
        # Execute watering
        is_successful = self.water_plant(relay, plan_obj.water_volume)
        
        # Set status based on result
        if is_successful:
            self.watering_status = s.Status(watering_status=True, message=s.MESSAGE_BASIC_PLAN_SUCCESS)
        else:
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INSUFFICIENT_WATER)

    def _execute_moisture_plan(self, plan: Union[Dict[str, Any], m.MoisturePlan], relay, sensors: Dict) -> None:
        """Execute a moisture-based watering plan."""
        logging.info(f"Executing moisture plan: {self.WATER_PLAN_MOISTURE}")
        
        # Convert dict to MoisturePlan object if needed
        if isinstance(plan, dict):
            plan_obj = m.MoisturePlan.from_json(j.dump_json(plan))
            self.running_plan = plan_obj
        else:
            self.running_plan = plan
            
        moisture_sensor = sensors.get(self.MOISTURE_SENSOR_KEY)
        self.water_plant_by_moisture(relay, moisture_sensor, self.running_plan)

    def _execute_time_plan(self, plan: Union[Dict[str, Any], t.TimePlan], relay) -> None:
        """Execute a time-based watering plan."""
        logging.info(f"Executing time plan: {self.WATER_PLAN_TIME}")
        
        # Convert dict to TimePlan object if needed
        if isinstance(plan, dict):
            plan_obj = t.TimePlan.from_json(j.dump_json(plan))
            self.running_plan = plan_obj
        else:
            self.running_plan = plan
            
        self.water_plant_by_timer(relay, self.running_plan)

    def _delete_running_plan(self) -> None:
        """Delete the currently running plan."""
        logging.info(f"Deleting running plan: {self.DELETE_RUNNING_PLAN}")
        self.running_plan = None
        self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_DELETED_PLAN)

    def _handle_invalid_plan(self, plan_type: str) -> None:
        """Handle invalid plan types."""
        logging.error(f"Invalid plan type: {plan_type}")
        self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INVALID_PLAN)

    def water_plant(self, relay, water_milliliters: int) -> bool:
        """
        Execute the actual watering operation.
        
        Args:
            relay: Relay control object
            water_milliliters: Amount of water to dispense
            
        Returns:
            True if watering was successful, False otherwise
        """
        # Check water availability
        if not self.is_water_level_sufficient(water_milliliters):
            logging.warning("Cannot water plant - insufficient water")
            return False
            
        # Calculate watering duration
        water_seconds = self.get_water_time_in_seconds_from_percent(water_milliliters)
        logging.info(f"Watering for {water_seconds} seconds ({water_milliliters}ml)")
        
        # Execute watering sequence
        try:
            relay.on()
            logging.info("Plant watering started")
            time.sleep(water_seconds)
            logging.info("Plant watering completed")
            return True
        except Exception as e:
            logging.error(f"Error during watering: {e}")
            return False
        finally:
            relay.off()
            logging.info("Relay turned off")

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan: m.MoisturePlan) -> None:
        """
        Water plant based on moisture sensor readings and timing constraints.
        
        Args:
            relay: Relay control object
            moisture_sensor: Moisture sensor object
            moisture_plan: Moisture-based watering plan
        """
        logging.info(f"Starting moisture-based watering with interval: {moisture_plan.check_interval}min")
        
        # Check timing constraints
        if not self._check_moisture_timing_constraints(moisture_plan.check_interval):
            return
            
        # Check moisture level and water if needed
        self._evaluate_moisture_and_water(relay, moisture_sensor, moisture_plan)

    def _check_moisture_timing_constraints(self, check_interval: int) -> bool:
        """
        Check if moisture watering timing constraints are met.
        
        Args:
            check_interval: Time interval in minutes between checks
            
        Returns:
            True if timing constraints are met, False otherwise
        """
        current_time_minus_delta = self.get_time().get_current_time_minus_delta(check_interval)
        logging.info(f"Current time minus delta: {current_time_minus_delta}")
        
        # Initialize water time if needed
        self._set_watered_time_if_none(current_time_minus_delta)
        
        # Check if time is out of range and reset if needed
        if self._is_water_time_out_of_range(check_interval):
            self._reset_water_time(current_time_minus_delta)
            
        # Verify timing constraint
        if self.water_time.time_last_watered != current_time_minus_delta:
            message = (f"Timing constraint not met: current_time_minus_delta={current_time_minus_delta}, "
                      f"water_time={self.water_time.time_last_watered}")
            logging.info(message)
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_PLAN_CONDITION_NOT_MET)
            return False
            
        return True

    def _evaluate_moisture_and_water(self, relay, moisture_sensor, moisture_plan: m.MoisturePlan) -> None:
        """
        Evaluate moisture level and execute watering if conditions are met.
        
        Args:
            relay: Relay control object
            moisture_sensor: Moisture sensor object
            moisture_plan: Moisture-based watering plan
        """
        moisture_level = self.get_moisture_level_in_percent()
        logging.info(f"Current moisture level: {moisture_level}% (sensor value: {moisture_sensor.value})")
        
        # Check if moisture is below threshold
        if moisture_level < moisture_plan.moisture_threshold:
            self._execute_moisture_watering(relay, moisture_sensor, moisture_plan)
        else:
            logging.info("Moisture level sufficient - no watering needed")
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_PLAN_CONDITION_NOT_MET)

    def _execute_moisture_watering(self, relay, moisture_sensor, moisture_plan: m.MoisturePlan) -> None:
        """
        Execute moisture-based watering operation.
        
        Args:
            relay: Relay control object
            moisture_sensor: Moisture sensor object
            moisture_plan: Moisture-based watering plan
        """
        water_milliliters = moisture_plan.water_volume
        
        # Check water availability
        if not self.is_water_level_sufficient(water_milliliters):
            logging.warning("Cannot water plant - insufficient water")
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INSUFFICIENT_WATER)
            return
            
        # Execute watering
        if self.water_plant(relay, water_milliliters):
            # Update tracking after successful watering
            self._update_moisture_watering_tracking(moisture_sensor)
            logging.info("Moisture-based watering completed successfully")
        else:
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INSUFFICIENT_WATER)

    def _update_moisture_watering_tracking(self, moisture_sensor) -> None:
        """Update time and moisture tracking after successful watering."""
        self.water_time.set_time_last_watered(self.get_time().get_current_time())
        self.moisture_level = moisture_sensor.value
        self.watering_status = s.Status(watering_status=True, message=s.MESSAGE_SUCCESS_MOISTURE)

    def _set_watered_time_if_none(self, current_time_minus_delta: str) -> None:
        """Initialize water time if it's None."""
        if self.water_time is None:
            self.water_time = self._create_time_keeper()
            self.water_time.set_time_last_watered(current_time_minus_delta)
            logging.info("Water time initialized")

    def _is_water_time_out_of_range(self, check_interval: int) -> bool:
        """
        Check if the last watering time is out of the acceptable range.
        
        Args:
            check_interval: Time interval in minutes between checks
            
        Returns:
            True if time is out of range, False otherwise
        """
        out_of_range_delta = check_interval * 2
        out_of_range_time = self.get_time().get_current_time_minus_delta(out_of_range_delta)
        
        logging.info(f"Checking time range: last_watered={self.water_time.time_last_watered}, "
                    f"out_of_range_time={out_of_range_time}")
        
        if self.water_time.time_last_watered < out_of_range_time:
            logging.info(f"Time {self.water_time.time_last_watered} is out of range "
                        f"(less than {out_of_range_time})")
            return True
        return False

    def _reset_water_time(self, current_time_minus_delta: str) -> None:
        """Reset water time to current time minus delta."""
        self.water_time = self._create_time_keeper()
        self.water_time.set_time_last_watered(current_time_minus_delta)
        logging.info(f"Water time reset to: {current_time_minus_delta}")

    def water_plant_by_timer(self, relay, time_plan: t.TimePlan) -> None:
        """
        Water plant based on scheduled times and days.
        
        Args:
            relay: Relay control object
            time_plan: Time-based watering plan
        """
        current_weekday = self._get_current_weekday()
        current_time = self.get_time().get_current_time()
        
        logging.info(f"Checking time-based watering: weekday={current_weekday}, time={current_time}")
        
        # Check each scheduled time in the plan
        for scheduled_time in time_plan.weekday_times:
            if self._should_execute_scheduled_watering(scheduled_time, current_weekday, current_time):
                self._execute_scheduled_watering(relay, time_plan, scheduled_time)
                return
                
        # No scheduled watering found
        logging.info("No scheduled watering time matches current conditions")
        self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_PLAN_CONDITION_NOT_MET)

    def _get_current_weekday(self) -> str:
        """Get current weekday name."""
        today = date.today()
        weekday = calendar.day_name[today.weekday()]
        logging.info(f"Current weekday: {weekday}")
        return weekday

    def _should_execute_scheduled_watering(self, scheduled_time, current_weekday: str, current_time: str) -> bool:
        """
        Check if scheduled watering should be executed.
        
        Args:
            scheduled_time: Scheduled watering time object
            current_weekday: Current weekday name
            current_time: Current time string
            
        Returns:
            True if watering should be executed, False otherwise
        """
        # Parse scheduled time
        water_time_obj = tk.TimeKeeper.get_time_from_time_string(scheduled_time.time_water)
        
        # Check weekday match
        if scheduled_time.weekday != current_weekday:
            return False
            
        # Check time match
        if water_time_obj != current_time:
            return False
            
        # Check if already watered today or at this time
        if (water_time_obj == self.water_time.time_last_watered and 
            self.get_date().get_current_date() == self.water_time.date_last_watered):
            logging.info("Already watered at this time today")
            return False
            
        return True

    def _execute_scheduled_watering(self, relay, time_plan: t.TimePlan, scheduled_time) -> None:
        """
        Execute scheduled watering operation.
        
        Args:
            relay: Relay control object
            time_plan: Time-based watering plan
            scheduled_time: Scheduled watering time object
        """
        logging.info(f"Executing scheduled watering: {scheduled_time} at {scheduled_time.time_water}")
        
        water_milliliters = time_plan.water_volume
        
        # Check water availability
        if not self.is_water_level_sufficient(water_milliliters):
            logging.warning("Cannot water plant - insufficient water")
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INSUFFICIENT_WATER)
            return
            
        # Execute watering
        if self.water_plant(relay, water_milliliters):
            # Update tracking after successful watering
            self._update_scheduled_watering_tracking(scheduled_time, time_plan)
            logging.info("Scheduled watering completed successfully")
        else:
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INSUFFICIENT_WATER)

    def _update_scheduled_watering_tracking(self, scheduled_time, time_plan: t.TimePlan) -> None:
        """Update tracking after successful scheduled watering."""
        water_time_obj = tk.TimeKeeper.get_time_from_time_string(scheduled_time.time_water)
        self.water_time.set_time_last_watered(water_time_obj)
        self.water_time.set_date_last_watered(self.get_date().get_current_date())
        self.watering_status = s.Status(watering_status=True, message=s.MESSAGE_SUCCESS_TIMER)
        
        # Clear plan if it should only execute once
        if time_plan.execute_only_once:
            self.running_plan = None
            logging.info("Plan cleared after single execution")

    def get_time(self) -> tk.TimeKeeper:
        """Get a new time keeper instance with current time."""
        time_keeper = tk.TimeKeeper(tk.TimeKeeper.get_current_time())
        logging.info(f"Created time keeper with current time: {time_keeper.get_current_time()}")
        return time_keeper

    def get_date(self) -> tk.TimeKeeper:
        """Get a new time keeper instance with current date."""
        date_keeper = tk.TimeKeeper(tk.TimeKeeper.get_current_date())
        logging.info(f"Created date keeper with current date: {date_keeper.get_current_date()}")
        return date_keeper

    def reset_water_level(self, capacity: int) -> None:
        """
        Reset water level to specified capacity.
        
        Args:
            capacity: New water capacity in milliliters
        """
        logging.info(f"Resetting water level: {self.water_level}ml -> {capacity}ml")
        self.water_level = capacity
        self.water_reset = True
        logging.info(f"Water level reset to {self.get_water_level_in_percent():.1f}%")

    def is_water_level_sufficient(self, water_milliliters: int) -> bool:
        """
        Check if there's sufficient water for the requested amount.
        
        Args:
            water_milliliters: Amount of water needed
            
        Returns:
            True if sufficient water is available, False otherwise
        """
        remaining_water = self.water_level - water_milliliters
        
        if remaining_water < 0:
            logging.warning(f"Insufficient water: need {water_milliliters}ml, have {self.water_level}ml")
            return False
            
        # Consume the water
        self.water_level = remaining_water
        logging.info(f"Water consumed: {water_milliliters}ml, remaining: {self.water_level}ml")
        return True

    def get_water_time_in_seconds_from_percent(self, water_milliliters: int) -> int:
        """
        Calculate watering duration in seconds based on water volume.
        
        Args:
            water_milliliters: Amount of water to dispense
            
        Returns:
            Duration in seconds
        """
        base_time = round(water_milliliters / self.water_pumped_in_second)
        
        # Add extra time after water reset for system stabilization
        if self.water_reset:
            base_time += 3
            self.water_reset = False
            logging.info("Added 3 seconds for water reset stabilization")
            
        logging.info(f"Calculated watering time: {base_time}s for {water_milliliters}ml")
        return base_time

    def get_moisture_level_in_percent(self) -> int:
        """
        Get current moisture level as percentage.
        
        Returns:
            Moisture level as integer percentage (0-100)
        """
        if self.moisture_sensor is None:
            logging.warning("Moisture sensor not available")
            return 0
            
        moisture_percent = round(100 - self.moisture_sensor.value * 100)
        logging.debug(f"Moisture level: {moisture_percent}% (sensor: {self.moisture_sensor.value})")
        return moisture_percent

    def get_water_level_in_percent(self) -> float:
        """
        Get current water level as percentage of capacity.
        
        Returns:
            Water level as float percentage (0.0-100.0)
        """
        if self.water_max_capacity <= 0:
            logging.warning("Invalid water max capacity")
            return 0.0
            
        water_percent = 100.0 * float(self.water_level) / float(self.water_max_capacity)
        logging.debug(f"Water level: {water_percent:.1f}% ({self.water_level}ml/{self.water_max_capacity}ml)")
        return water_percent

    def get_running_plan(self) -> Optional[Union[p.Plan, m.MoisturePlan, t.TimePlan]]:
        """
        Get the currently running plan.
        
        Returns:
            Current running plan or None if no plan is active
        """
        return self.running_plan
