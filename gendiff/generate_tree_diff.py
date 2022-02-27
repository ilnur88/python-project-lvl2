from gendiff.consts import FIRST_VAL, SECOND_VAL, EVEN_VAL, MINUS_VAL, PLUS_VAL


def encode_value(value):
    if type(value) == bool:
        return str(value).lower()
    if value is None:
        return 'null'
    return str(value)


def generate_tree_diff_from_structire(str_dict):
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