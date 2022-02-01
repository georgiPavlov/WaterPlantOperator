import logging
from time import sleep


class IServerCheckerInterface:

    def plan_executor(self, **sensors):
        pass

    def send_result(self, moisture_level, status, water_level):
        pass

    def show(self):
        raise Exception("NotImplementedException")


class ServerChecker(IServerCheckerInterface):

    def __init__(self, pump, communicator, wait_time_between_cycle):
        self.pump = pump
        self.communicator = communicator
        self.wait_time_between_cycle = wait_time_between_cycle
        IServerCheckerInterface.__init__(self)

    def plan_executor(self, **sensors):
        while True:
            try:
                plan = self.communicator.get_plan()
                running_plan = self.pump.get_running_plan()
                logging.info(f'Running plan: {running_plan}')
                if plan == self.communicator.return_emply_json():
                    logging.info(f'No new plan for execution found: {running_plan}')
                    if running_plan is None:
                        logging.info('running plan for found')
                        continue

                status = self.pump.execute_water_plan(plan, **sensors)
                water_level = self.pump.get_water_level_in_percent()
                moisture_level = self.pump.get_moisture_level_in_percent()
                self.send_result(moisture_level, status, water_level)
                sleep(self.wait_time_between_cycle)
                logging.info('Executed watering loop')
            except Exception as e:
                logging.info('[Exception]' + str(e))

    def send_result(self, moisture_level, status, water_level):
        self.communicator.post_plan_execution(status)
        self.communicator.post_water(water_level)
        self.communicator.post_moisture(moisture_level)
        # self.communicator.post_picture(picture)
