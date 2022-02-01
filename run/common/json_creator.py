import json
import logging


def get_json(json_string):
    logging.info(f'get_json func road: {json_string}')
    return json.loads(json_string)


def dump_json(json_string):
    logging.info(f'dump_json func road: {json_string}')
    json.dumps(json_string)
