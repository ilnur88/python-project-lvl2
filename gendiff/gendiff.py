import json
import yaml

FIRST_VAL = 'first_val'
SECOND_VAL = 'second_val'
EVEN_VAL = 'even_val'
MINUS_VAL = 'minus_val'
PLUS_VAL = 'plus_val'


def encode_value(value):
    if type(value) == bool:
        return str(value).lower()
    if value is None:
        return 'null'
    return str(value)

def transform_to_temp_dict(temp_dict, input_dict, value):    
    for key, val in input_dict.items():
        if key not in temp_dict:
            temp_dict[key] = {}
        if isinstance(val, dict):
            if 'children' not in temp_dict[key]:
                child_dict = dict()
            else:
                child_dict = temp_dict[key]['children']
            transform_to_temp_dict(child_dict, val, value)
            temp_dict[key]['children'] = child_dict            
            temp_dict[key][value] = '+'
        else:
            temp_dict[key][value] = val

def add_even_vals(child_dict, index):
    return_dict = dict()
    for key, val in child_dict.items():
        if isinstance(val, dict):
            if key not in return_dict:
                return_dict[key] = {}
            if 'children' in val:
                return_dict[key][EVEN_VAL] = '+'
                return_dict[key]['children'] = add_even_vals(val['children'], index)                
            else:
                return_dict[key][EVEN_VAL] = val[index]
    return return_dict


def from_temp_dict_generate_diff(temp_dict):
    return_dict = dict()
    for key, val in temp_dict.items():
        if isinstance(val, dict):            
            if key not in return_dict:
                return_dict[key] = {}
            if 'children' in val:
                if FIRST_VAL in val and SECOND_VAL in val:
                    if val[FIRST_VAL] != val[SECOND_VAL]:
                        if val[FIRST_VAL] != '+':
                            return_dict[key][MINUS_VAL] = val[FIRST_VAL]
                            return_dict[key][PLUS_VAL] = '+'
                            return_dict[key]['children'] = add_even_vals(val['children'], SECOND_VAL)
                        else:
                            return_dict[key][PLUS_VAL] = val[SECOND_VAL]
                            return_dict[key][MINUS_VAL] = '+'
                            return_dict[key]['children'] = add_even_vals(val['children'], FIRST_VAL)
                    else:
                        return_dict[key][EVEN_VAL] = '+'
                        return_dict[key]['children'] = from_temp_dict_generate_diff(val['children'])                   

                if FIRST_VAL in val and SECOND_VAL not in val:
                    return_dict[key][MINUS_VAL] = '+'
                    return_dict[key]['children'] = add_even_vals(val['children'], FIRST_VAL)
                if FIRST_VAL not in val and SECOND_VAL in val:
                    return_dict[key][PLUS_VAL] = '+'
                    return_dict[key]['children'] = add_even_vals(val['children'], SECOND_VAL)                
            else:
                if FIRST_VAL in val and SECOND_VAL in val:
                    if val[FIRST_VAL] == val[SECOND_VAL]:
                        return_dict[key][EVEN_VAL] = val[FIRST_VAL]
                    else:
                        return_dict[key][MINUS_VAL] = val[FIRST_VAL]
                        return_dict[key][PLUS_VAL] = val[SECOND_VAL]                
                if FIRST_VAL in val and SECOND_VAL not in val:
                    return_dict[key][MINUS_VAL] = val[FIRST_VAL]
                if FIRST_VAL not in val and SECOND_VAL in val:
                    return_dict[key][PLUS_VAL] = val[SECOND_VAL]                
    return return_dict

def generate_diff_structure(dict1, dict2):
    temp_dict = dict()
    transform_to_temp_dict(temp_dict, dict1, FIRST_VAL)    
    transform_to_temp_dict(temp_dict, dict2, SECOND_VAL)
    temp_dict1 = from_temp_dict_generate_diff(temp_dict)
    return temp_dict1

def generate_string_from_structire(str_dict):
    def walk(element, depth):
        return_str = ''
        for (k, v) in sorted(element.items(), key = lambda x : x[0]):
            prefix = ' ' * (depth - 1) * 4
            if 'children' in v:
                if EVEN_VAL in v:
                    diff_prefix = '  {} '.format(' ')
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': {' + walk(v['children'], depth + 1) + '\n' + ' ' * depth * 4 + '}'
                if MINUS_VAL in v and v[MINUS_VAL] == '+':
                    diff_prefix = '  {} '.format('-')
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': {' + walk(v['children'], depth + 1) + '\n' + ' ' * depth * 4 + '}'
                if MINUS_VAL in v and v[MINUS_VAL] != '+':
                    diff_prefix = '  {} '.format('-')
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': ' + v[MINUS_VAL]
                if PLUS_VAL in v and v[PLUS_VAL] == '+':
                    diff_prefix = '  {} '.format('+')
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': {' + walk(v['children'], depth + 1) + '\n' + ' ' * depth * 4 + '}'
                if PLUS_VAL in v and v[PLUS_VAL] != '+':
                    diff_prefix = '  {} '.format('+')
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': ' + v[PLUS_VAL]
            else:
                diff_prefix = ''
                if EVEN_VAL in v:
                    diff_prefix = '  {} '.format(' ')
                    output = encode_value(v[EVEN_VAL])
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': ' + output
                if MINUS_VAL in v:
                    diff_prefix = '  {} '.format('-')
                    output = encode_value(v[MINUS_VAL])
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': ' + output
                if PLUS_VAL in v:
                    diff_prefix = '  {} '.format('+')
                    output = encode_value(v[PLUS_VAL])
                    return_str = return_str + '\n' + prefix + diff_prefix + k + ': ' + output                
        return return_str              

    return '{' + walk(str_dict, 1) + '\n}'

def generate_diff(filepath1, filepath2):
    if filepath1.endswith('.json'):
        file1_dict = json.load(open(filepath1))
    if filepath1.endswith('.yaml') or filepath1.endswith('.yml'):
        file2_dict = yaml.load(open(filepath1))

    if filepath2.endswith('.json'):
        file2_dict = json.load(open(filepath2))
    if filepath2.endswith('.yaml') or filepath2.endswith('.yml'):
        file2_dict = yaml.load(open(filepath2))

    diff = generate_diff_structure(file1_dict, file2_dict)
    #return diff

    return generate_string_from_structire(diff)
    print( generate_string_from_structire(diff))
