from json import dumps
from gendiff.data import get_name_type_value, get_children


def prepare_to_print_plaint(diff):
    result = walk(diff, '')
    result = [item.strip() for item in result if item]
    return '\n'.join(result)


def walk(items, path):
    result = []
    for item in items:
        name, type_, value = get_name_type_value(item)
        new_path = f'{path}{name}'
        if type_ == 'added':
            value_str = make_str_from_value(value)
            line = f"Property '{new_path}' was added with value: {value_str}"
            result.append(line)
        elif type_ == 'removed':
            line = f"Property '{new_path}' was removed"
            result.append(line)
        elif type_ == 'nested':
            children = get_children(item)
            line = '\n'.join(walk(children, f'{new_path}.'))
            result.append(line)
        elif type_ == 'changed':
            value_1, value_2 = value
            value_1_str = make_str_from_value(value_1)
            value_2_str = make_str_from_value(value_2)
            line = f"Property '{new_path}' was updated." \
                   f" From {value_1_str} to {value_2_str}"
            result.append(line)
    return result


def make_str_from_value(value):
    if isinstance(value, dict):
        value = '[complex value]'
    elif isinstance(value, bool) or value is None:
        value = dumps(value)
    elif isinstance(value, str):
        value = f"'{value.strip()}'"
    return str(value)
