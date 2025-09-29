"""
Server checker module for water plant automation system.

This module provides the main execution loop that coordinates between the pump,
server communication, and sensor operations.
"""
import logging
from time import sleep
from typing import Dict, Any, Optional
import run.common.json_creator as j
import run.model.status as st
from run.operation.camera_op import PHOTO_ID, CAMERA_KEY


class IServerCheckerInterface:
    """Interface defining the contract for server checker operations."""

    def plan_executor(self, **sensors) -> None:
        """Execute the main plan execution loop."""
        pass

    def send_result(self, moisture_level: int, status: st.Status, water_level: float) -> None:
        """Send execution results to the server."""
        pass

    def show(self) -> None:
        """Display current status (not implemented)."""
        raise NotImplementedError("show method not implemented")


class ServerChecker(IServerCheckerInterface):
    """
    Main server checker class that coordinates watering operations.
    
    This class manages the main execution loop, handles server communication,
    and coordinates between pump operations and sensor readings.
    """
    
    # Constants
    WATER_CONST = 'water'

    def __init__(self, pump, communicator, wait_time_between_cycle: int):
        """
        Initialize the server checker.
        
        Args:
            pump: Pump instance for watering operations
            communicator: Server communicator for API calls
            wait_time_between_cycle: Wait time in seconds between execution cycles
        """
        super().__init__()
        
        self.pump = pump
        self.communicator = communicator
        self.wait_time_between_cycle = wait_time_between_cycle
        
        logging.info(f"ServerChecker initialized with {wait_time_between_cycle}s cycle time")

    def plan_executor(self, **sensors) -> None:
        """
        Execute the main plan execution loop.
        
        This method runs continuously, handling:
        - Health checks
        - Water level management
        - Photo capture requests
        - Plan execution
        - Result reporting
        
        Args:
            **sensors: Sensor objects (moisture_sensor, camera, etc.)
        """
        self.pump.moisture_sensor = sensors.get(self.pump.MOISTURE_SENSOR_KEY)
        
        logging.info("Starting main execution loop")
        
        while True:
            try:
                self._execute_cycle(sensors)
                sleep(self.wait_time_between_cycle)
                logging.info("Execution cycle completed\n" + "="*50)
            except Exception as e:
                logging.error(f"Exception in execution cycle: {e}")

    def _execute_cycle(self, sensors: Dict[str, Any]) -> None:
        """
        Execute a single cycle of the main loop.
        
        Args:
            sensors: Dictionary of sensor objects
        """
        # Send health check
        self._send_health_check()
        
        # Handle water level updates
        self._handle_water_level_update()
        
        # Handle photo capture requests
        self._handle_photo_capture(sensors)
        
        # Execute watering plan
        self._execute_watering_plan(sensors)

    def _send_health_check(self) -> None:
        """Send health check status to server."""
        health_status = st.Status(watering_status=False, message=st.HEALTH_CHECK)
        self.communicator.post_plan_execution(health_status)
        logging.debug("Health check sent")

    def _handle_water_level_update(self) -> None:
        """Handle water level updates from server."""
        water_level_json = self.communicator.get_water_level()
        logging.info(f"Water level from server: {water_level_json}")
        
        if water_level_json != self.communicator.return_emply_json():
            water_level_value = water_level_json[self.WATER_CONST]
            logging.info(f"Resetting water level to: {water_level_value}ml")
            
            # Update pump capacity and reset water level
            self.pump.water_max_capacity = water_level_value
            self.pump.reset_water_level(water_level_value)
            
            # Report updated water level to server
            current_percent = self.pump.get_water_level_in_percent()
            self.communicator.post_water(current_percent)
            logging.info(f"Water level reset to {current_percent:.1f}%")

    def _handle_photo_capture(self, sensors: Dict[str, Any]) -> None:
        """
        Handle photo capture requests from server.
        
        Args:
            sensors: Dictionary of sensor objects
        """
        photo_json = self.communicator.get_picture()
        logging.info(f"Photo capture request: {photo_json}")
        
        if photo_json != self.communicator.return_emply_json():
            photo_name = photo_json[PHOTO_ID]
            logging.info(f"Taking photo: {photo_name}")
            
            # Capture photo using camera sensor
            camera = sensors.get(CAMERA_KEY)
            if camera:
                camera.take_photo(photo_name)
                logging.info(f"Photo captured: {photo_name}")
                
                # Send photo confirmation to server
                self.communicator.post_picture(photo_name)
                logging.info(f"Photo confirmation sent: {photo_name}")
            else:
                logging.warning("Camera sensor not available")

    def _execute_watering_plan(self, sensors: Dict[str, Any]) -> None:
        """
        Execute watering plan based on server requests or running plans.
        
        Args:
            sensors: Dictionary of sensor objects
        """
        # Get plan from server
        plan = self.communicator.get_plan()
        running_plan = self.pump.get_running_plan()
        
        logging.info(f"Server plan: {plan}, Running plan: {running_plan}")
        
        # Determine which plan to execute
        plan_to_execute = self._determine_plan_to_execute(plan, running_plan)
        
        if plan_to_execute is None:
            # No plan to execute - send regular moisture reading
            self._send_regular_moisture_reading()
            return
            
        # Execute the plan
        logging.info(f"Executing plan: {plan_to_execute}")
        status = self.pump.execute_water_plan(plan_to_execute, **sensors)
        
        # Send results
        water_level = self.pump.get_water_level_in_percent()
        moisture_level = self.pump.get_moisture_level_in_percent()
        self.send_result(moisture_level, status, water_level)

    def _determine_plan_to_execute(self, server_plan: Dict[str, Any], running_plan) -> Optional[Dict[str, Any]]:
        """
        Determine which plan should be executed.
        
        Args:
            server_plan: Plan received from server
            running_plan: Currently running plan
            
        Returns:
            Plan to execute or None if no plan should be executed
        """
        # If server has a new plan, use it
        if server_plan != self.communicator.return_emply_json():
            return server_plan
            
        # If no server plan but we have a running plan, continue with it
        if running_plan is not None:
            logging.info("Continuing with running plan")
            return running_plan
            
        # No plan to execute
        logging.info("No plan available for execution")
        return None

    def _send_regular_moisture_reading(self) -> None:
        """Send regular moisture reading when no plan is active."""
        logging.info("No active plan - sending regular moisture reading")
        moisture_level = self.pump.get_moisture_level_in_percent()
        self.communicator.post_moisture(moisture_level)
        logging.info(f"Regular moisture reading sent: {moisture_level}%")

    def send_result(self, moisture_level: int, status: st.Status, water_level: float) -> None:
        """
        Send execution results to the server.
        
        Args:
            moisture_level: Current moisture level percentage
            status: Execution status from pump
            water_level: Current water level percentage
        """
        logging.info(f"Sending results: moisture={moisture_level}%, water={water_level:.1f}%, status={status}")
        
        # Send all results to server
        self.communicator.post_plan_execution(status)
        self.communicator.post_water(water_level)
        self.communicator.post_moisture(moisture_level)
        
        logging.info("Results sent to server successfully")



