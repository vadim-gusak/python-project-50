from gendiff.data import get_name, get_name_type_value


def prepare_to_print_stylish(diff: list):
    result = '\n'.join(walk(diff, 0))
    return '{\n' + result + '\n}'


def walk(items, step):
    result = []
    if isinstance(items, list):
        for item in sorted(items, key=get_name):
            name, type_, value = get_name_type_value(item)
            lines = make_string_from_node(name, value, step, type_)
            result.append(lines)
    elif isinstance(items, dict):
        items_sorted = dict(sorted(items.items()))
        for key, value in items_sorted.items():
            lines = make_string_from_node(key, value, step)
            result.append(lines)
    return result


def make_string_from_node(name, value, step, type_='unchanged'):
    end = f"\n{step * '  '}    " + '}'
    if type_ == 'nested' or (type_ == 'unchanged' and isinstance(value, dict)):
        lines = f'{step * "  "}    {name}: ' + '{\n'
        walk_result = '\n'.join(walk(value, step + 2))
        lines += walk_result + end
    elif type_ == 'added' or type_ == 'removed':
        sign = '+' if type_ == 'added' else '-'
        begin = f'{step * "  "}  {sign} {name}: '
        return begin + normalize_value(value) \
            if not isinstance(value, dict) \
            else begin + '{\n' + '\n'.join(walk(value, step + 2)) + end
    elif type_ == 'changed':
        value_1, value_2 = value
        begin_1 = f'{step * "  "}  - {name}: '
        begin_2 = f'\n{step * "  "}  + {name}: '
        if isinstance(value_1, dict):
            walk_result = '\n'.join(walk(value_1, step + 2))
            end_1 = '{\n' + walk_result + end
            end_2 = f'{normalize_value(value_2)}'
        elif isinstance(value_2, dict):
            walk_result = '\n'.join(walk(value_2, step + 2))
            end_1 = f'{normalize_value(value_1)}'
            end_2 = '{\n' + walk_result + end
        else:
            end_1 = f'{normalize_value(value_1)}'
            end_2 = f'{normalize_value(value_2)}'
        return begin_1 + end_1 + begin_2 + end_2
    else:
        lines = f'{step * "  "}    {name}: {normalize_value(value)}'
    return lines


def normalize_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return value.strip()
    return str(value)
