import run.common.json_creator as jc
from run.model.plan import Plan


class TimePlan(Plan):
    def __init__(self, name, plan_type, water_volume, timer):
        self.timer = timer
        Plan.__init__(self, name, plan_type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        json_dict = jc.get_json(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'