import json


def JSON_ENCODE(key, value):
    if type(value) == bool:
        return '{} : {}'.format(key, str(value).lower())    
    return '{} : {}'.format(key, value)


def generate_diff(filepath1, filepath2):
    json1 = json.load(open(filepath1))
    json2 = json.load(open(filepath2))

    resultdict = dict()

    for key, value in json1.items():
        if key in json2:
            if json1[key] == json2[key]:
                resultdict['{}'.format(JSON_ENCODE(key, value))] = ' '
            else:
                resultdict['{}'.format(JSON_ENCODE(key, value))] = '-'
                resultdict['{}'.format(JSON_ENCODE(key, json2[key]))] = '+'
        else:
            resultdict['{}'.format(JSON_ENCODE(key, value))] = '-'

    for key, value in json2.items():
        if key not in json1:
            resultdict['{}'.format(JSON_ENCODE(key, value))] = '+'

    result_str = '{\n'

    list_keys = list(resultdict.keys())
    list_keys.sort()

    for key in list_keys:
        result_str = result_str + '    {} {}'.format(resultdict[key], key) + '\n'
    result_str = result_str + '}'
    return result_str

