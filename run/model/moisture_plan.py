import run.common.json_creator as jc
from run.model.plan import Plan


class MoisturePlan(Plan):
    def __init__(self, name, plan_type, water_volume, moisture_threshold, check_interval):
        self.moisture_threshold = moisture_threshold
        self.check_interval = check_interval
        Plan.__init__(self, name, plan_type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        json_dict = jc.get_json(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'
