import time
from datetime import date
import calendar

import run.sensor.relay as Relay
from run.common import time_keeper as TK
from run.model import time_plan as tk


class Pump:
    def __init__(self):
        self.water_time = self.get_time()
        self.water_time.set_time_last_watered(self.water_time.get_current_time())

    def water_plant(self, relay, seconds):
        relay.on()
        print("Plant is being watered!")
        time.sleep(seconds)
        print("Watering is finished!")
        relay.off()

    def water_plant_by_moisture(self, relay, seconds, moisture, moisture_plan):
        check_int = moisture_plan.check_interval
        print(f'check_int: {check_int}')
        current_time_with_delta = self.get_time().get_current_time_with_delta(check_int)
        print(f'current_time: {current_time_with_delta}')
        if self.water_time.time_last_watered != current_time_with_delta:
            print(f'current time is: {current_time_with_delta} and water time is {self.water_time}')
            return

        print("moisture is {}".format(moisture.value))
        if moisture.is_dry():
            self.water_plant(relay, seconds)
            self.water_time.set_time_last_watered(self.get_time().get_current_time())

    def water_plant_by_timer(self, relay, seconds, time_plan):
        timer = time_plan.timer
        today = date.today()
        weekday = calendar.day_name[today.weekday()]
        print(f'current weekday {weekday}')
        current_time = self.get_time().get_current_time()
        print(f'current time {current_time}')

        if timer.weekday == weekday and timer.time == current_time:
            self.water_plant(relay, seconds)
        else:
            print("water plant check passed without execution water operation")


    def get_time(self):
        time = TK.TimeKeeper(TK.TimeKeeper.get_current_time())
        print(f'init current time at: {time.get_current_time()}')
        return time.get_current_time()



