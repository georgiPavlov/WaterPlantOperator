import json


class Device:

    def __init__(self, device_id):
        self.device_id = device_id

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<device_id {self.device_id}>'
