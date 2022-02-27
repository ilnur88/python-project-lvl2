from gendiff.consts import FIRST_VAL, SECOND_VAL, EVEN_VAL, MINUS_VAL, PLUS_VAL
import json


def encode_value(value):
    if type(value) == bool:
        return str(value).lower()
    if value is None:
        return 'null'
    return str(value)


def generate_json_diff_from_structire(str_dict):
    json_obj = json.dumps(str_dict, indent=4)
    return json_obj