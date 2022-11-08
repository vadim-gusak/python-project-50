from gendiff.data import get_name_type_value, get_name
from json import dumps


def prepare_to_print_json_format(diff):
    def walk(item):
        name, type_, value = get_name_type_value(item)
        if type_ == 'unchanged':
            return {name: value}
        elif type_ == 'added' or type_ == 'removed':
            return {f'{name}_{type_}': value}
        elif type_ == 'changed':
            value_1, value_2 = value
            return {f'{name}_old': value_1, f'{name}_updated': value_2}
        else:
            value_sorted = sorted(value, key=get_name)
            walk_result = list(map(walk, value_sorted))
            return {name: walk_result}
    diff_sorted = sorted(diff, key=get_name)
    result = list(map(walk, diff_sorted))
    return dumps(result, sort_keys=True, indent=2)
