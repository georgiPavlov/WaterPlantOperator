from types import SimpleNamespace
from typing import List

import run.common.json_creator as jc
from run.model.plan import Plan
from run.model.watertime import WaterTime
from typing import List


class TimePlan(Plan):
    water_times: List[WaterTime]

    def __init__(self, name, plan_type, water_volume, water_times: List[WaterTime]) -> None:
        self.water_times = water_times
        Plan.__init__(self, name, plan_type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        time_plan = jc.get_json_sm(json_string)
        return cls(time_plan.name, time_plan.plan_type, time_plan.water_volume, time_plan.water_times)

    def __repr__(self):
        return f'<name {self.name}>'


plan = '''{"name": "plant1", "plan_type": "basic", "water_volume": 200,
        "water_times":[{"weekday": "Friday", "time_water": "08:40 pm"}]}'''

json = TimePlan.from_json(plan)
print(json)
for obj in json.water_times:
    print(f'{obj.time_water}  plus {obj.weekday}')

