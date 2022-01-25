import json

import plan as Plan


class TimePlan(Plan):
    def __init__(self, name, type, water_volume, timer):
        self.Timer = timer
        Plan.__init__(name, type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'