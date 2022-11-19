from json import dumps
from gendiff.data import get_name, get_name_type_value


def prepare_to_print_stylish(diff: list):
    result = '\n'.join(walk(diff, 0))
    return '{\n' + result + '\n}'


def walk(items, depth):
    result = []
    if isinstance(items, list):
        for item in sorted(items, key=get_name):
            name, type_, value = get_name_type_value(item)
            lines = make_string_from_node(name, value, depth, type_)
            result.append(lines)
    elif isinstance(items, dict):
        items_sorted = dict(sorted(items.items()))
        for name, value in items_sorted.items():
            lines = make_string_from_node(name, value, depth)
            result.append(lines)
    return result


def make_string_from_node(name, value, depth, type_='unchanged'):
    if type_ == 'nested':
        result = make_str_from_value(depth, ' ', name, value)
    elif type_ == 'added' or type_ == 'removed':
        sign = '+' if type_ == 'added' else '-'
        result = make_str_from_value(depth, sign, name, value)
    elif type_ == 'changed':
        value_1, value_2 = value
        lines_1 = make_str_from_value(depth, '-', name, value_1)
        lines_2 = make_str_from_value(depth, '+', name, value_2)
        result = f'{lines_1}\n{lines_2}'
    else:
        result = make_str_from_value(depth, ' ', name, value)
    return result


def make_str_from_value(depth, sign, name, value):
    begin = f'{depth * "    "}  {sign} {name}: '
    if isinstance(value, dict) or isinstance(value, list):
        walk_result = '\n'.join(walk(value, depth + 1))
        end = f"\n{depth * '    '}    " + '}'
        result = begin + '{\n' + walk_result + end
    elif isinstance(value, bool) or value is None:
        result = begin + dumps(value)
    else:
        result = begin + str(value).strip()
    return result
