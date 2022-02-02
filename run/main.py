import logging
from run.sensor.relay import Relay
from run.sensor.moisture_sensor import Moisture
from run.http_communicator.server_communicator import ServerCommunicator
from run.operation.pump import Pump
from run.operation.server_checker import ServerChecker

WATER_PUMPED_IN_SECOND = 10
MOISTURE_MAX_LEVEL = 0
WATER_TIME_BETWEEN_CYCLE = 10
WATER_MAX_CAPACITY = 2000
MOISTURE_PIN = 4
RELAY_PIN = 12
DEVICE_GUID = 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e'


def main():
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting....")
    relay = Relay(RELAY_PIN, active_high=False)
    moisture = Moisture(MOISTURE_PIN, charge_time_limit=0.2, threshold=0.6)

    pump = Pump(water_max_capacity=WATER_MAX_CAPACITY, water_pumped_in_second=WATER_PUMPED_IN_SECOND,
                moisture_max_level=MOISTURE_MAX_LEVEL)
    sever_communicator = ServerCommunicator(device_guid=DEVICE_GUID)
    server_checker = ServerChecker(pump=pump, communicator=sever_communicator,
                                   wait_time_between_cycle=WATER_TIME_BETWEEN_CYCLE)
    logging.info("executor starting..")
    server_checker.plan_executor(**{pump.RELAY_SENSOR_KEY: relay, pump.MOISTURE_SENSOR_KEY: moisture})
    logging.info("end")


# program starter
main()
