import json


def get_json(json_string):
    print(f'get_json func road: {json_string}')
    return json.loads(json_string)
