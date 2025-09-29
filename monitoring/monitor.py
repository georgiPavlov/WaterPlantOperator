#!/usr/bin/env python3
"""
Container Monitoring Script for WaterPlantOperator
Monitors the health and status of the WaterPlantOperator container
"""

import requests
import time
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContainerMonitor:
    """Monitor for WaterPlantOperator container"""
    
    def __init__(self, operator_url: str = "http://waterplant-operator:8000"):
        self.operator_url = operator_url
        self.health_endpoint = f"{operator_url}/health"
        self.status_endpoint = f"{operator_url}/status"
        self.monitoring_interval = 30  # seconds
        self.retry_count = 3
        self.retry_delay = 5  # seconds
    
    def check_health(self) -> bool:
        """Check if the operator is healthy"""
        try:
            response = requests.get(self.health_endpoint, timeout=10)
            if response.status_code == 200:
                logger.info("Health check passed")
                return True
            else:
                logger.warning(f"Health check failed with status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get operator status"""
        try:
            response = requests.get(self.status_endpoint, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Status check failed with status: {response.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Status check failed: {e}")
            return {}
    
    def log_status(self, status: Dict[str, Any]):
        """Log the current status"""
        if status:
            logger.info("=== Operator Status ===")
            logger.info(f"Timestamp: {status.get('timestamp', 'N/A')}")
            logger.info(f"Environment: {status.get('environment', 'N/A')}")
            logger.info(f"Simulation Mode: {status.get('simulation_mode', 'N/A')}")
            
            # Log sensor readings
            sensors = status.get('sensors', {})
            if sensors:
                logger.info("Sensor Readings:")
                for sensor, value in sensors.items():
                    logger.info(f"  {sensor}: {value}")
            
            # Log relay states
            relays = status.get('relays', {})
            if relays:
                logger.info("Relay States:")
                for relay, state in relays.items():
                    logger.info(f"  {relay}: {'ON' if state else 'OFF'}")
            
            # Log camera status
            camera = status.get('camera', {})
            if camera:
                logger.info(f"Camera Available: {camera.get('available', False)}")
                logger.info(f"Camera Recording: {camera.get('recording', False)}")
        else:
            logger.warning("No status data available")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info(f"Starting container monitoring for {self.operator_url}")
        logger.info(f"Monitoring interval: {self.monitoring_interval} seconds")
        
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        while True:
            try:
                # Check health
                if self.check_health():
                    consecutive_failures = 0
                    
                    # Get and log status
                    status = self.get_status()
                    self.log_status(status)
                    
                    # Log system metrics
                    self.log_system_metrics()
                    
                else:
                    consecutive_failures += 1
                    logger.warning(f"Health check failed ({consecutive_failures}/{max_consecutive_failures})")
                    
                    if consecutive_failures >= max_consecutive_failures:
                        logger.error("Too many consecutive health check failures. Exiting.")
                        sys.exit(1)
                
                # Wait for next check
                time.sleep(self.monitoring_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in monitoring loop: {e}")
                time.sleep(self.retry_delay)
    
    def log_system_metrics(self):
        """Log system metrics"""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            logger.info("=== System Metrics ===")
            logger.info(f"CPU Usage: {cpu_percent}%")
            logger.info(f"Memory Usage: {memory_percent}%")
            logger.info(f"Disk Usage: {disk_percent}%")
            
        except ImportError:
            logger.warning("psutil not available for system metrics")
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")

def main():
    """Main function"""
    import os
    
    # Get operator URL from environment
    operator_url = os.getenv('OPERATOR_URL', 'http://waterplant-operator:8000')
    
    # Create and start monitor
    monitor = ContainerMonitor(operator_url)
    monitor.monitor_loop()

if __name__ == "__main__":
    main()
