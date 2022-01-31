import time
from datetime import date
import calendar
from run.common import time_keeper as tk
import run.model.status as s


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

    def get_moisture_level_in_percent(self):
        pass

    def get_water_level_in_percent(self):
        pass


class Pump(IPumpInterface):
    WATER_PUMPED_IN_SECOND = 10
    WATER_PLAN_BASIC = 'basic'
    WATER_PLAN_TIME = 'time'
    WATER_PLAN_MOISTURE = 'moisture'
    DELETE_RUNNING_PLAN = 'delete'
    RELAY_SENSOR_KEY = 'relay'
    MOISTURE_SENSOR_KEY = 'moisture_sensor'
    WATER_MAX_CAPACITY = 2000
    MOISTURE_MAX_LEVEL = 0

    def __init__(self):
        IPumpInterface.__init__(self)
        self.water_time = self.get_time()
        self.water_time.set_time_last_watered(self.water_time.get_current_time())
        self.water_level = self.WATER_MAX_CAPACITY
        self.moisture_level = self.MOISTURE_MAX_LEVEL
        self.running_plan = None
        self.watering_status = None

    def execute_water_plan(self, plan, **sensors):
        plan_type = plan.plan_type
        relay = sensors.get(self.RELAY_SENSOR_KEY)
        if plan_type == self.WATER_PLAN_BASIC:
            print(f'option: {self.WATER_PLAN_BASIC}')
            is_watering_successful = self.water_plant(relay, plan.water_volume)
            if is_watering_successful:
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
            else:
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_BASIC_PLAN_SUCCESS}')
        elif plan_type == self.WATER_PLAN_MOISTURE:
            self.running_plan = plan
            print(f'option: {self.WATER_PLAN_MOISTURE}')
            moisture_sensor = sensors.get(self.MOISTURE_SENSOR_KEY)
            self.water_plant_by_moisture(relay, moisture_sensor, self.running_plan)
        elif plan_type == self.WATER_PLAN_TIME:
            self.running_plan = plan
            print(f'option: {self.WATER_PLAN_TIME}')
            self.water_plant_by_timer(relay, self.running_plan)
        elif plan_type == self.DELETE_RUNNING_PLAN:
            self.running_plan = None
            print(f'option: {self.DELETE_RUNNING_PLAN}')
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_DELETED_PLAN)
        else:
            print(f'invalid plan type: {plan_type}')
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INVALID_PLAN)
        return self.watering_status

    def water_plant(self, relay, water_milliliters):
        if not self.is_water_level_sufficient(water_milliliters):
            print("[moisture plan] can not water plant")
            return False
        water_seconds = self.get_water_time_in_seconds_from_percent(water_milliliters)
        print(f'water_seconds: {water_seconds}')
        relay.on()
        print("Plant is being watered!")
        time.sleep(water_seconds)
        print("Watering is finished!")
        relay.off()
        return True

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan):
        check_int = moisture_plan.check_interval
        print(f'check_int: {check_int}')
        current_time_with_delta = self.get_time().get_current_time_with_delta(check_int)
        print(f'current_time: {current_time_with_delta}')
        if self.water_time.time_last_watered != current_time_with_delta:
            message = f'current time is: {current_time_with_delta} and water time is {self.water_time}'
            print(message)
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')
            return

        print("moisture is {}".format(moisture_sensor.value))
        if moisture_sensor.is_dry():
            water_milliliters = moisture_plan.water_volume
            if not self.is_water_level_sufficient(water_milliliters):
                print("[moisture plan] can not water plant")
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
                return
            self.water_plant(relay, water_milliliters)
            self.water_time.set_time_last_watered(self.get_time().get_current_time())
            print('moisture plan: watering successful')
            self.moisture_level = moisture_sensor.value
            self.watering_status = s.Status(watering_status=True, message=f'{s.MESSAGE_SUCCESS_MOISTURE}')
            return
        self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')
        print('returning only moisture')

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
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
                return
            self.water_plant(relay, water_milliliters)
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_SUCCESS_TIMER}')
        else:
            print("water plant check passed without execution water operation")
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')

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

    def get_moisture_level_in_percent(self):
        return round(100 - self.moisture_level * 100)

    def get_water_level_in_percent(self):
        return 100 * float(self.water_level) / float(self.WATER_MAX_CAPACITY)

    def get_running_plan(self):
        return self.running_plan

