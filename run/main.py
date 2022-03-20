import logging

from run.operation import camera_op
from run.sensor.relay import Relay
from run.sensor.moisture_sensor import Moisture
from run.sensor.camera_sensor import Camera, initCamera
from run.http_communicator.server_communicator import ServerCommunicator
from run.operation.pump import Pump
from run.operation.server_checker import ServerChecker
from pathlib import Path

WATER_PUMPED_IN_SECOND = 10
MOISTURE_MAX_LEVEL = 0
WATER_TIME_BETWEEN_CYCLE = 10
WATER_MAX_CAPACITY = 2000
MOISTURE_PIN = 4
RELAY_PIN = 12
DEVICE_GUID = 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e'
PHOTO_DIR = '/tmp/device/photos'
DELAY_BETWEEN_PHOTO_TAKEN = 5


def main():
    logging.root.handlers = []
    logging.basicConfig(filename='/tmp/example.log', filemode='w', level=logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting....")
    Path(PHOTO_DIR).mkdir(parents=True, exist_ok=True)
    relay = Relay(RELAY_PIN, active_high=False)
    moisture = Moisture(MOISTURE_PIN, charge_time_limit=0.2, threshold=0.6)

    pump = Pump(water_max_capacity=WATER_MAX_CAPACITY, water_pumped_in_second=WATER_PUMPED_IN_SECOND,
                moisture_max_level=MOISTURE_MAX_LEVEL)
    sever_communicator = ServerCommunicator(device_guid=DEVICE_GUID, photos_dir=PHOTO_DIR)
    server_checker = ServerChecker(pump=pump, communicator=sever_communicator,
                                   wait_time_between_cycle=WATER_TIME_BETWEEN_CYCLE)

    camera = Camera(camera_instance=initCamera, photos_dir=PHOTO_DIR,
                    wait_before_still_in_seconds=DELAY_BETWEEN_PHOTO_TAKEN)

    logging.info("executor starting..")
    server_checker.plan_executor(**{pump.RELAY_SENSOR_KEY: relay, pump.MOISTURE_SENSOR_KEY: moisture,
                                    camera_op.CAMERA_KEY: camera})
    logging.info("end")


# program starter
main()
