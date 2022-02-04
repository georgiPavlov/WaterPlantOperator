import json
import logging
from types import SimpleNamespace


def get_json(json_string):
    logging.info(f'get_json func road: {json_string}')
    return json.loads(json_string)


def get_json_sm(json_string):
    logging.info(f'get_json func road: {json_string}')
    return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))


def dump_json(json_string):
    logging.info(f'dump_json func road: {json_string}')
    return json.dumps(json_string)
