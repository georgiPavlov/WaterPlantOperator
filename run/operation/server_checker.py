import logging
from time import sleep
import run.common.json_creator as j
import run.model.status as st
from run.operation.camera_op import PHOTO_ID, CAMERA_KEY


class IServerCheckerInterface:

    def plan_executor(self, **sensors):
        pass

    def send_result(self, moisture_level, status, water_level):
        pass

    def show(self):
        raise Exception("NotImplementedException")


class ServerChecker(IServerCheckerInterface):
    WATER_CONST = 'water'

    def __init__(self, pump, communicator, wait_time_between_cycle, ):
        self.pump = pump
        self.communicator = communicator
        self.wait_time_between_cycle = wait_time_between_cycle
        IServerCheckerInterface.__init__(self)

    def plan_executor(self, **sensors):
        self.pump.moisture_sensor = sensors.get(self.pump.MOISTURE_SENSOR_KEY)
        while True:
            try:
                health_status = st.Status(watering_status=False, message=st.HEALTH_CHECK)
                self.communicator.post_plan_execution(health_status)
                water_level_json = self.communicator.get_water_level()
                logging.info(f'Water level from server: {water_level_json}')
                if water_level_json != self.communicator.return_emply_json():
                    water_level_value = water_level_json[self.WATER_CONST]
                    logging.info(f'Resetting water: {water_level_value}')
                    self.pump.water_max_capacity = water_level_value
                    self.pump.reset_water_level(water_level_value)
                    logging.info(f'resetting water to {self.pump.get_water_level_in_percent()}')
                    self.communicator.post_water(self.pump.get_water_level_in_percent())
                photo_json = self.communicator.get_picture()

                logging.info(f'Photo for capture: {photo_json}')
                if photo_json != self.communicator.return_emply_json():
                    photo_name_ = photo_json[PHOTO_ID]
                    logging.info(f'Taking photo: {photo_name_}')
                    camera = sensors.get(CAMERA_KEY)
                    camera.take_photo(photo_name_)
                    logging.info(f'Photo taken: {photo_name_}')
                    self.communicator.post_picture(photo_name_)
                    logging.info(f'Photo send: {photo_name_}')
                plan = self.communicator.get_plan()
                running_plan = self.pump.get_running_plan()
                logging.info(f'Running plan: {running_plan}')
                if plan == self.communicator.return_emply_json():
                    logging.info(f'No new plan for execution found: {running_plan}')
                    if running_plan is None:
                        logging.info('running plan not found')
                        logging.info('sending regular moisture from check')
                        moisture_level = self.pump.get_moisture_level_in_percent()
                        self.communicator.post_moisture(moisture_level)
                        sleep(self.wait_time_between_cycle)
                        continue
                    else:
                        plan = running_plan
                logging.info(f'Getting status: {running_plan}')
                status = self.pump.execute_water_plan(plan, **sensors)
                water_level = self.pump.get_water_level_in_percent()
                moisture_level = self.pump.get_moisture_level_in_percent()
                self.send_result(moisture_level, status, water_level)
                sleep(self.wait_time_between_cycle)
                logging.info('Executed watering loop\n\n\n')
            except Exception as e:
                logging.info('[Exception]' + str(e))

    def send_result(self, moisture_level, status, water_level):
        self.communicator.post_plan_execution(status)
        self.communicator.post_water(water_level)
        self.communicator.post_moisture(moisture_level)



