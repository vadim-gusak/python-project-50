def prepare_to_print_plaint(diff):
    result = list(map(lambda item: walk(item, ''), diff))
    result = [item for item in flatten(result) if item]
    result.sort()
    return '\n'.join(result)


def walk(item, path):
    line = ''
    type_ = item.get('type')
    if type_:
        name = item.get('name')
        path = update_path(name, path)
        if type_ == 'added' or type_ == 'removed':
            return make_line_added_or_removed(item, path)
        elif type_ == 'changed':
            return make_line_changed(item, path)
        elif type_ == 'nested':
            children = item['value']
            return list(map(lambda i: walk(i, path), children))
    return line


def update_path(name, path):
    if path != '':
        result = path + '.' + name
    else:
        result = name
    return result


def flatten(some_list):
    result = []
    for item in some_list:
        if isinstance(item, list):
            new_items = flatten(item)
            result += new_items
        else:
            result.append(item)
    return result


def make_line_added_or_removed(item, path):
    line_begin = f"Property '{path}' was "
    type_ = item['type']
    value = item['value']
    if type_ == 'removed':
        return f'{line_begin}{type_}'
    elif isinstance(value, dict) and type_ == 'added':
        return f'{line_begin}added with value: [complex value]'
    return f'{line_begin}{type_} with value: {update_value(value)}'


def make_line_changed(item, path):
    line_begin = f"Property '{path}' was "
    value_1, value_2 = item['value']
    if not isinstance(value_1, dict) and not isinstance(value_2, dict):
        return f'{line_begin}updated. From {update_value(value_1)}' \
               f' to {update_value(value_2)}'
    if isinstance(value_1, dict):
        return f'{line_begin}updated. From [complex value] to ' \
               f'{update_value(value_2)}'
    if isinstance(value_2, dict):
        return f'{line_begin}updated. From {update_value(value_1)} to ' \
               f'[complex value]'


def update_value(value):
    if value == 'true' or value == 'false' or value == 'null':
        return value
    if isinstance(value, str):
        return f"'{value.strip()}'"
    return str(value)