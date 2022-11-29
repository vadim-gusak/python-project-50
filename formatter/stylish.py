from json import dumps
from gendiff.data import get_name_type_value, get_children


def prepare_to_print_stylish(diff: list):
    return '{\n' + walk(diff, 0) + '\n}'


def walk(items, depth):
    result = []
    for item in items:
        name, type_, value = get_name_type_value(item)
        if type_ == 'nested':
            children = get_children(item)
            lines = make_str_from_children(name, children, depth)
        elif type_ == 'added' or type_ == 'removed':
            sign = '+' if type_ == 'added' else '-'
            lines = make_str_from_value(depth, sign, name, value)
        elif type_ == 'changed':
            value_1, value_2 = value
            lines_1 = make_str_from_value(depth, '-', name, value_1)
            lines_2 = make_str_from_value(depth, '+', name, value_2)
            lines = f'{lines_1}\n{lines_2}'
        else:
            lines = make_str_from_value(depth, ' ', name, value)
        result.append(lines)
    return '\n'.join(result)


def make_str_from_value(depth, sign, name, value):
    begin = f'{depth * "    "}  {sign} {name}: '
    if isinstance(value, dict):
        middle = make_str_from_dict(value, depth)
        end = f"\n{depth * '    '}    " + '}'
        result = begin + '{\n' + middle + end
    elif isinstance(value, bool) or value is None:
        result = begin + dumps(value)
    else:
        result = begin + str(value).strip()
    return result


def make_str_from_dict(dict_, depth):
    result = []
    dict_sorted = dict(sorted(dict_.items()))
    for name, value in dict_sorted.items():
        result.append(make_str_from_value(depth + 1, ' ', name, value))
    return '\n'.join(result)


def make_str_from_children(name, children, depth):
    begin = f'{depth * "    "}    {name}: ' + '{\n'
    walk_result = walk(children, depth + 1)
    end = f"\n{depth * '    '}    " + '}'
    return begin + walk_result + end
