from gendiff.data import get_name, get_children, get_value, get_diff


def prepare_to_print_stylish(diff):
    def walk(item, step):
        name = get_name(item)
        value = get_value(item)
        value_1, value_2 = value
        children = sorted(get_children(item), key=get_name)
        node_diff = get_diff(item)
        lines = ''
        line_begin = f"{step * '  '}  "
        if node_diff is None and not children:
            lines = f'{line_begin}  {name}: {value_1}'
        if node_diff == 'check' and not children:
            lines = f'{line_begin}- {name}: {value_1}\n'
            lines += f'{line_begin}+ {name}: {value_2}'
        if node_diff == 'removed' and not children:
            lines = f'{line_begin}- {name}: {value_1}'
        if node_diff == 'check' and not (value_1 is None) and value_2 is None and children:
            lines = f'{line_begin}- {name}: {value_1}\n'
            lines += f'{line_begin}+ {name}: ' + '{\n'
            walks = list(map(lambda node: walk(node, step + 2), children))
            lines += '\n'.join(walks) + '\n'
            lines += line_begin + '  }'
        if node_diff == 'added' and not children:
            lines = f'{line_begin}+ {name}: {value_2}'
        if node_diff == 'check' and value_1 is None and not (value_2 is None) and children:
            lines = f'{line_begin}- {name}: ' + '{\n'
            walks = list(map(lambda node: walk(node, step + 2), children))
            lines += '\n'.join(walks) + '\n'
            lines += line_begin + '  }\n'
            lines += f'{line_begin}+ {name}: {value_2}'
        if children and value_1 is None and value_2 is None:
            sign = choose_sign(node_diff)
            lines = f'{line_begin}{sign} {name}: ' + '{\n'
            walks = list(map(lambda node: walk(node, step + 2), children))
            lines += '\n'.join(walks) + '\n'
            lines += line_begin + '  }'
        return lines
    diff_sorted = sorted(diff, key=get_name)
    result = list(map(lambda node: walk(node, 0), diff_sorted))
    return '{\n' + '\n'.join(result) + '\n}'


def choose_sign(diff):
    if diff == 'added':
        return '+'
    if diff == 'removed':
        return '-'
    return ' '
