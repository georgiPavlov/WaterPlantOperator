import json


class Plant:
    def __init__(self, name, type, water_volume):
        self.name = name
        self.type = type
        self.water_volume = water_volume

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<name {self.name}>'








json_string = '''{
    "name": "plant1",
    "type": "basic",
    "water_volum": "200ml",
}'''

plant_list = []
with open('data.json', 'r') as json_file:
    user_data = json.loads(json_file.read())
    for u in user_data:
        plant_list.append(Plant(**u))

print(plant_list)
