import run.operation.pump as p
import run.http.server_communicator as com
from time import sleep


class IServerCheckerInterface:

    def check_for_new_plan(self, **sensors):
        pass

    def send_result(self):
        pass

    def show(self):
        raise Exception("NotImplementedException")


class ServerCheckerInterface(IServerCheckerInterface):

    def __init__(self, pump, communicator, wait_time_between_cycle):
        self.pump = pump
        self.communicator = communicator
        self.wait_time_between_cycle = wait_time_between_cycle
        IServerCheckerInterface.__init__(self)

    def check_for_new_plan(self, **sensors):
        while True:
            try:
                plan = self.communicator.get_plan()
                running_plan = self.pump.get_running_plan()
                if plan == self.communicator.return_emply_json() or running_plan is None:
                    continue

                status = self.pump.execute_water_plan(plan, **sensors)
                water_level = self.pump.get_water_level_in_percent()
                moisture_level = self.pump.get_moisture_level_in_percent()
                self.communicator.post_plan_execution(status)
                self.communicator.post_water(water_level)
                self.communicator.post_moisture(moisture_level)
                # self.communicator.post_picture(picture)

                sleep(self.wait_time_between_cycle)
                print('Executed watering loop')
            except Exception as e:
                print('[Exception]' + str(e))
