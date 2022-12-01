from json import dumps
from gendiff.data import get_name_type_value, get_children


def prepare_to_print_stylish(diff: list) -> str:
    return '{\n' + walk(diff, 0) + '\n}'


def walk(items: list, depth: int) -> str:
    result = []
    for item in items:
        name, type_, value = get_name_type_value(item)
        if type_ == 'nested':
            children = get_children(item)
            lines = make_string(depth, ' ', name, children=children)
        elif type_ == 'added' or type_ == 'removed':
            sign = '+' if type_ == 'added' else '-'
            lines = make_string(depth, sign, name, value)
        elif type_ == 'changed':
            value_1, value_2 = value
            lines_1 = make_string(depth, '-', name, value_1)
            lines_2 = make_string(depth, '+', name, value_2)
            lines = f'{lines_1}\n{lines_2}'
        else:
            lines = make_string(depth, ' ', name, value)
        result.append(lines)
    return '\n'.join(result)


def make_string(depth: int, sign: str, name: str,
                value=None, children=None) -> str:
    begin = f'{depth * "    "}  {sign} {name}: '
    end = f"\n{depth * '    '}    " + '}'
    if children:
        walk_result = walk(children, depth + 1)
        result = begin + '{\n' + walk_result + end
    elif isinstance(value, dict):
        lines = []
        value_sorted = dict(sorted(value.items()))
        for name, value in value_sorted.items():
            lines.append(make_string(depth + 1, ' ', name, value))
        result = begin + '{\n' + '\n'.join(lines) + end
    elif isinstance(value, bool) or value is None:
        result = begin + dumps(value)
    else:
        result = begin + str(value).strip()
    return result
