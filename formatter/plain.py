from gendiff.data import get_name_type_value, get_name


def prepare_to_print_plaint(diff):
    result = walk(diff, '')
    result = [item.strip() for item in result if item]
    return '\n'.join(result)


def walk(items, path):
    result = []
    items_sorted = sorted(items, key=get_name)
    for item in items_sorted:
        name, type_, value = get_name_type_value(item)
        new_path = f'{path}{name}'
        if type_ == 'added':
            value = update_value(value)
            line = f"Property '{new_path}' was added with value: {value}"
            result.append(line)
        elif type_ == 'removed':
            line = f"Property '{new_path}' was removed"
            result.append(line)
        elif type_ == 'nested':
            line = '\n'.join(walk(value, f'{new_path}.'))
            result.append(line)
        elif type_ == 'changed':
            value_1, value_2 = value
            value_1, value_2 = update_value(value_1), update_value(value_2)
            line = f"Property '{new_path}' was updated." \
                   f" From {value_1} to {value_2}"
            result.append(line)
    return result


def update_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return f"'{value.strip()}'"
    return str(value)
