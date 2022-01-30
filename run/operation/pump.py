import time
from datetime import date
import calendar
from run.common import time_keeper as tk


class IPumpInterface:

    def execute_water_plan(self, plan, **sensors):
        pass

    def is_water_level_sufficient(self, water_milliliters):
        pass

    def water_plant(self, relay, water_milliliters):
        pass

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan):
        pass

    def water_plant_by_timer(self, relay, time_plan):
        pass

    def get_water_time_in_seconds_from_percent(self, water_milliliters):
        pass


class Pump(IPumpInterface):
    WATER_PUMPED_IN_SECOND = 10
    WATER_PLAN_BASIC = 'basic'
    WATER_PLAN_TIME = 'time'
    WATER_PLAN_MOISTURE = 'moisture'
    RELAY_SENSOR_KEY = 'relay'
    MOISTURE_SENSOR_KEY = 'moisture_sensor'
    WATER_MAX_CAPACITY = 2000

    def __init__(self):
        IPumpInterface.__init__(self)
        self.water_time = self.get_time()
        self.water_time.set_time_last_watered(self.water_time.get_current_time())
        self.water_level = self.WATER_MAX_CAPACITY

    def execute_water_plan(self, plan, **sensors):
        plan_type = plan.plan_type
        relay = sensors.get(self.RELAY_SENSOR_KEY)
        if plan_type == self.WATER_PLAN_BASIC:
            print(f'option: {self.WATER_PLAN_BASIC}')
            self.water_plant(relay, plan.water_volume)
        elif plan_type == self.WATER_PLAN_MOISTURE:
            print(f'option: {self.WATER_PLAN_MOISTURE}')
            moisture_sensor = sensors.get(self.MOISTURE_SENSOR_KEY)
            self.water_plant_by_moisture(relay, moisture_sensor, plan)
        elif plan_type == self.WATER_PLAN_TIME:
            print(f'option: {self.WATER_PLAN_TIME}')
            self.water_plant_by_timer(relay, plan)
        else:
            print(f'invalid plan type: {plan_type}')

    def water_plant(self, relay, water_milliliters):
        if not self.is_water_level_sufficient(water_milliliters):
            print("[moisture plan] can not water plant")
            return
        water_seconds = self.get_water_time_in_seconds_from_percent(water_milliliters)
        print(f'water_seconds: {water_seconds}')
        relay.on()
        print("Plant is being watered!")
        time.sleep(water_seconds)
        print("Watering is finished!")
        relay.off()

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan):
        check_int = moisture_plan.check_interval
        print(f'check_int: {check_int}')
        current_time_with_delta = self.get_time().get_current_time_with_delta(check_int)
        print(f'current_time: {current_time_with_delta}')
        if self.water_time.time_last_watered != current_time_with_delta:
            print(f'current time is: {current_time_with_delta} and water time is {self.water_time}')
            return

        print("moisture is {}".format(moisture_sensor.value))
        if moisture_sensor.is_dry():
            water_milliliters = moisture_plan.water_volume
            if not self.is_water_level_sufficient(water_milliliters):
                print("[moisture plan] can not water plant")
                return
            self.water_plant(relay, water_milliliters)
            self.water_time.set_time_last_watered(self.get_time().get_current_time())
            print('moisture plan: watering successful')
            return moisture_sensor.value
        print('returning only moisture')
        return moisture_sensor.value

    def water_plant_by_timer(self, relay, time_plan):
        timer = time_plan.timer
        today = date.today()
        weekday = calendar.day_name[today.weekday()]
        print(f'current weekday {weekday}')
        current_time = self.get_time().get_current_time()
        print(f'current time {current_time}')

        if timer.weekday == weekday and timer.time == current_time:
            water_milliliters = time_plan.water_volume
            if not self.is_water_level_sufficient(water_milliliters):
                print("[moisture plan] can not water plant")
                return
            self.water_plant(relay, water_milliliters)
        else:
            print("water plant check passed without execution water operation")

    def get_time(self):
        time_k = tk.TimeKeeper(tk.TimeKeeper.get_current_time())
        print(f'init current time at: {time_k.get_current_time()}')
        return time_k.get_current_time()

    def reset_water_level(self):
        print(f'reseting water: current water level: {self.water_level}')
        self.water_level = self.WATER_MAX_CAPACITY

    def is_water_level_sufficient(self, water_milliliters):
        if self.water_level - water_milliliters < 0:
            print(f'insufficient water capacity: {self.water_level - water_milliliters}')
            return False
        self.water_level -= water_milliliters
        return True

    def get_water_time_in_seconds_from_percent(self, water_milliliters):
        return round(water_milliliters / self.WATER_PUMPED_IN_SECOND)
