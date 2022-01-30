import json


def get_json(json_string):
    print(f'get_json func road: {json_string}')
    return json.loads(json_string)


def dump_json(json_string):
    print(f'dump_json func road: {json_string}')
    json.dumps(json_string)
