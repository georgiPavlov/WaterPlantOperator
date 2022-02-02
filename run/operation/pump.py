import time
import logging
from datetime import date
import calendar
from run.common import time_keeper as tk
import run.model.status as s
import run.model.plan as p
import run.model.moisture_plan as m
import run.model.time_plan as t
import run.common.json_creator as j


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
    WATER_PLAN_BASIC = 'basic'
    WATER_PLAN_TIME = 'time'
    WATER_PLAN_MOISTURE = 'moisture'
    DELETE_RUNNING_PLAN = 'delete'
    RELAY_SENSOR_KEY = 'relay'
    MOISTURE_SENSOR_KEY = 'moisture_sensor'
    PLAN_TYPE_KEY = 'plan_type'

    def __init__(self, water_max_capacity, water_pumped_in_second, moisture_max_level):
        IPumpInterface.__init__(self)
        self.water_time = self.get_time()
        self.water_time.set_time_last_watered(self.water_time.get_current_time())
        self.water_max_capacity = water_max_capacity
        self.water_level = self.water_max_capacity
        self.moisture_level = moisture_max_level
        self.water_pumped_in_second = water_pumped_in_second
        self.running_plan = None
        self.watering_status = None

    def execute_water_plan(self, plan, **sensors):
        logging.info(plan)
        plan_type = plan[self.PLAN_TYPE_KEY]
        relay = sensors.get(self.RELAY_SENSOR_KEY)
        if plan_type == self.WATER_PLAN_BASIC:
            logging.info(f'option: {self.WATER_PLAN_BASIC}')
            plan_obj = p.Plan.from_json(j.dump_json(plan))
            is_watering_successful = self.water_plant(relay, plan_obj.water_volume)
            if is_watering_successful:
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
            else:
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_BASIC_PLAN_SUCCESS}')
        elif plan_type == self.WATER_PLAN_MOISTURE:
            plan_obj = m.MoisturePlan.from_json(j.dump_json(plan))
            self.running_plan = plan_obj
            logging.info(f'option: {self.WATER_PLAN_MOISTURE}')
            moisture_sensor = sensors.get(self.MOISTURE_SENSOR_KEY)
            self.water_plant_by_moisture(relay, moisture_sensor, self.running_plan)
        elif plan_type == self.WATER_PLAN_TIME:
            plan_obj = t.TimePlan.from_json(j.dump_json(plan))
            self.running_plan = plan_obj
            logging.info(f'option: {self.WATER_PLAN_TIME}')
            self.water_plant_by_timer(relay, self.running_plan)
        elif plan_type == self.DELETE_RUNNING_PLAN:
            self.running_plan = None
            logging.info(f'option: {self.DELETE_RUNNING_PLAN}')
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_DELETED_PLAN)
        else:
            logging.info(f'invalid plan type: {plan_type}')
            self.watering_status = s.Status(watering_status=False, message=s.MESSAGE_INVALID_PLAN)
        return self.watering_status

    def water_plant(self, relay, water_milliliters):
        if not self.is_water_level_sufficient(water_milliliters):
            logging.info("[moisture plan] can not water plant")
            return False
        water_seconds = self.get_water_time_in_seconds_from_percent(water_milliliters)
        logging.info(f'water_seconds: {water_seconds}')
        relay.on()
        logging.info("Plant is being watered!")
        time.sleep(water_seconds)
        logging.info("Watering is finished!")
        relay.off()
        return True

    def water_plant_by_moisture(self, relay, moisture_sensor, moisture_plan):
        check_int = moisture_plan.check_interval
        logging.info(f'check_int: {check_int}')
        current_time_with_delta = self.get_time().get_current_time_with_delta(check_int)
        logging.info(f'current_time: {current_time_with_delta}')
        if self.water_time.time_last_watered != current_time_with_delta:
            message = f'current time is: {current_time_with_delta} and water time is {self.water_time}'
            logging.info(message)
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')
            return

        logging.info("moisture is {}".format(moisture_sensor.value))
        if moisture_sensor.is_dry():
            water_milliliters = moisture_plan.water_volume
            if not self.is_water_level_sufficient(water_milliliters):
                logging.info("[moisture plan] can not water plant")
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
                return
            self.water_plant(relay, water_milliliters)
            self.water_time.set_time_last_watered(self.get_time().get_current_time())
            logging.info('moisture plan: watering successful')
            self.moisture_level = moisture_sensor.value
            self.watering_status = s.Status(watering_status=True, message=f'{s.MESSAGE_SUCCESS_MOISTURE}')
            return
        self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')
        logging.info('returning only moisture')

    def water_plant_by_timer(self, relay, time_plan):
        timer = time_plan.timer
        today = date.today()
        weekday = calendar.day_name[today.weekday()]
        logging.info(f'current weekday {weekday}')
        current_time = self.get_time().get_current_time()
        logging.info(f'current time {current_time}')

        if timer.weekday == weekday and timer.time == current_time:
            water_milliliters = time_plan.water_volume
            if not self.is_water_level_sufficient(water_milliliters):
                logging.info("[moisture plan] can not water plant")
                self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_INSUFFICIENT_WATER}')
                return
            self.water_plant(relay, water_milliliters)
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_SUCCESS_TIMER}')
        else:
            logging.info("water plant check passed without execution water operation")
            self.watering_status = s.Status(watering_status=False, message=f'{s.MESSAGE_PLAN_CONDITION_NOT_MET}')

    def get_time(self):
        time_k = tk.TimeKeeper(tk.TimeKeeper.get_current_time())
        logging.info(f'init current time at: {time_k.get_current_time()}')
        return time_k

    def reset_water_level(self):
        logging.info(f'reseting water: current water level: {self.water_level}')
        self.water_level = self.water_max_capacity

    def is_water_level_sufficient(self, water_milliliters):
        if self.water_level - water_milliliters < 0:
            logging.info(f'insufficient water capacity: {self.water_level - water_milliliters}')
            return False
        self.water_level -= water_milliliters
        return True

    def get_water_time_in_seconds_from_percent(self, water_milliliters):
        return round(water_milliliters / self.water_pumped_in_second)

    def get_moisture_level_in_percent(self):
        return round(100 - self.moisture_level * 100)

    def get_water_level_in_percent(self):
        return 100 * float(self.water_level) / float(self.water_max_capacity)

    def get_running_plan(self):
        return self.running_plan

