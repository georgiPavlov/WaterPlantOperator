import json

import Plan as Plan


class MoisturePlan(Plan):
    def __init__(self, name, type, water_volume, moisture_threshold, check_interval):
        self.moisture_threshold = moisture_threshold
        self.check_interval = check_interval
        Plan.__init__(name, type, water_volume)

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'
