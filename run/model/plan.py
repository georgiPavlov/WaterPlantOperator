import logging
import run.common.json_creator as jc


class Plan:
    def __init__(self, name, plan_type, water_volume):
        self.name = name
        self.plan_type = plan_type
        self.water_volume = water_volume

    @classmethod
    def from_json(cls, json_string1):
        json_dict = jc.get_json(json_string1)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'


json_string = '''{"name": "plant1", "plan_type": "basic", "water_volume": "200ml"}'''

plan_t = Plan.from_json(json_string)
logging.info(plan_t.plan_type)