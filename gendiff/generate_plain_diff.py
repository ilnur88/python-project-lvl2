from gendiff.consts import EVEN_VAL, MINUS_VAL, PLUS_VAL


def encode_value(value, value_str):
    if 'children' in value and value[value_str] == '+':
        return '[complex value]'
    if type(value[value_str]) == bool:
        return str(value[value_str]).lower()
    if value[value_str] is None:
        return 'null'
    if value[value_str] is dict:
        return '+'
    return '\'' + str(value[value_str]) + '\''


def get_path(path, new_value):
    return '{}.{}'.format(path, new_value).lstrip('.')


def generate_plain_diff_from_structire(str_dict):
    def walk(element, path):
        return_str = ''
        for (k, v) in sorted(element.items(), key=lambda x: x[0]):
            if EVEN_VAL in v and 'children' in v:
                return_str += walk(v['children'], get_path(path, k))
            if MINUS_VAL in v and PLUS_VAL in v:
                return_str += 'Property \'{}\' was updated. From {} to {}'.\
                    format(
                        get_path(path, k),
                        encode_value(v, MINUS_VAL),
                        encode_value(v, PLUS_VAL)
                        ) + '\n'
            else:
                if MINUS_VAL in v:
                    return_str += 'Property \'{}\' was removed'.\
                        format(get_path(path, k)) + '\n'
                if PLUS_VAL in v:
                    return_str += 'Property \'{}\' was added with value: {}'.\
                        format(
                            get_path(path, k),
                            encode_value(v, PLUS_VAL)
                            ) + '\n'
        return return_str

    return walk(str_dict, '').rstrip('\n')
