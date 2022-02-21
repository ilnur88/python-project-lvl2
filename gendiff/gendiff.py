import json
import yaml


def JSON_ENCODE(key, value):
    if type(value) == bool:
        return '{} : {}'.format(key, str(value).lower())    
    return '{} : {}'.format(key, value)


def generate_diff(filepath1, filepath2):
    json1 = json.load(open(filepath1))
    json2 = json.load(open(filepath2))

    result_str = '{\n'

    for key, value in json1.items():
        if key in json2:
            if json1[key] == json2[key]:
                result_str = result_str + '  {} {}'.format(' ', JSON_ENCODE(key, value)) + '\n'
            else:
                result_str = result_str + '  {} {}'.format('-', JSON_ENCODE(key, value)) + '\n'
                result_str = result_str + '  {} {}'.format('+', JSON_ENCODE(key, json2[key])) + '\n'
        else:
            result_str = result_str + '  {} {}'.format('-', JSON_ENCODE(key, value)) + '\n'

    for key, value in json2.items():
        if key not in json1:
            result_str = result_str + '  {} {}'.format('+', JSON_ENCODE(key, value)) + '\n'
    
    return result_str + '}'


def generate_diff_yaml(filepath1, filepath2):
    yaml1 = yaml.load(open(filepath1))
    yaml2 = yaml.load(open(filepath2))

    result_str = '{\n'

    for key, value in yaml1.items():
        if key in yaml2:
            if yaml1[key] == yaml2[key]:
                result_str = result_str + '  {} {}'.format(' ', JSON_ENCODE(key, value)) + '\n'
            else:
                result_str = result_str + '  {} {}'.format('-', JSON_ENCODE(key, value)) + '\n'
                result_str = result_str + '  {} {}'.format('+', JSON_ENCODE(key, yaml2[key])) + '\n'
        else:
            result_str = result_str + '  {} {}'.format('-', JSON_ENCODE(key, value)) + '\n'

    for key, value in yaml2.items():
        if key not in yaml1:
            result_str = result_str + '  {} {}'.format('+', JSON_ENCODE(key, value)) + '\n'
    
    return result_str + '}'

