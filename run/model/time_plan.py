from types import SimpleNamespace
from typing import List

import run.common.json_creator as jc
from run.model.plan import Plan
from run.model.watertime import WaterTime
from typing import List


class TimePlan(Plan):
    weekday_times: List[WaterTime]
    execute_only_once: bool

    def __init__(self, name, plan_type, water_volume, weekday_times: List[WaterTime], execute_only_once: bool) -> None:
        self.weekday_times = weekday_times
        self.execute_only_once = execute_only_once
        Plan.__init__(self, name, plan_type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        time_plan = jc.get_json_sm(json_string)
        return cls(time_plan.name, time_plan.plan_type, time_plan.water_volume, time_plan.weekday_times,
                   time_plan.execute_only_once)

    def __repr__(self):
        return f'<name {self.name}>'


# plan = '''{"name": "plant1", "plan_type": "basic", "water_volume": 200,
#        "weekday_times":[{"weekday": "Friday", "time_water": "08:40 pm"}]}'''
#
# json = TimePlan.from_json(plan)
# print(json)
# for obj in json.weekday_times:
#    print(f'{obj.time_water}  plus {obj.weekday}')

