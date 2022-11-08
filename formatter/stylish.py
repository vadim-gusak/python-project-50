from gendiff.data import get_name_type_value, get_name


def prepare_to_print_stylish(diff):
    diff_sorted = sorted(diff, key=lambda item: item['name'])
    result = list(map(lambda node: walk(node, 0), diff_sorted))
    return '{\n' + '\n'.join(result) + '\n}'


def walk(item, step):
    name, type_, value = get_name_type_value(item)
    lines = ''
    if type_ == 'nested':
        lines += make_line(step, ' ', name, '{') + '\n'
        value_sorted = sorted(value, key=get_name)
        walk_result = list(map(lambda i: walk(i, step + 2), value_sorted))
        lines += '\n'.join(walk_result)
        lines += f"\n{step * '  '}    " + '}'
    elif type_ == 'added' or type_ == 'removed' or type_ == 'unchanged':
        lines += make_lines_added_removed_or_unchanged(item, step)
    if type_ == 'changed':
        lines += make_lines_changed(item, step)
    return lines


def make_lines_added_removed_or_unchanged(item, step):
    name, type_, value = get_name_type_value(item)
    sign = ' '
    if type_ == 'added':
        sign = '+'
    elif type_ == 'removed':
        sign = '-'
    if isinstance(value, dict):
        result = make_line(step, sign, name, '{\n')
        result += make_lines_dicts(step + 2, value)
        result += f"\n{step * '  '}    " + '}'
        return result
    value = update_value(value)
    return make_line(step, sign, name, value)


def make_lines_changed(item, step):
    name, type_, value = get_name_type_value(item)
    value_1, value_2 = value
    result = ''
    if not isinstance(value_1, dict) and not isinstance(value_2, dict):
        value_1 = update_value(value_1)
        value_2 = update_value(value_2)
        result = make_line(step, '-', name, f'{value_1}\n')
        result += make_line(step, '+', name, value_2)
    elif isinstance(value_1, dict):
        value_2 = update_value(value_2)
        result = make_line(step, '-', name, '{\n')
        result += make_lines_dicts(step + 2, value_1)
        result += f"\n{step * '  '}    " + '}\n'
        result += make_line(step, '+', name, value_2)
    elif isinstance(value_2, dict):
        value_1 = update_value(value_1)
        result = make_line(step, '-', name, f'{value_1}\n')
        result += make_line(step, '+', name, '{\n')
        result += make_lines_dicts(step + 2, value_2)
        result += f"\n{step * '  '}    " + '}'
    return result


def make_line(step, sign, name, end):
    return f'{step * "  "}  {sign} {name}: {end}'


def make_lines_dicts(step, dicts):
    dicts_sorted = dict(sorted(dicts.items()))
    result = []
    for key, value in dicts_sorted.items():
        if isinstance(value, dict):
            result.append(make_line(step, ' ', key, '{'))
            result.append(make_lines_dicts(step + 2, value))
            result.append(f"{step * '  '}    " + '}')
            continue
        result.append(make_line(step, ' ', key, value))
    return '\n'.join(result)


def update_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return value.strip()
    return value
