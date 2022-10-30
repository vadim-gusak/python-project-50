from gendiff.data import get_name, get_children, get_value, get_diff


def prepare_to_print_stylish(diff):
    diff_sorted = sorted(diff, key=get_name)
    result = list(map(lambda node: walk(node, 0), diff_sorted))
    return '{\n' + '\n'.join(result) + '\n}'


def walk(item, step):
    name = get_name(item)
    value = get_value(item)
    children = sorted(get_children(item), key=get_name)
    node_diff = get_diff(item)
    line_begin = f"{step * '  '}  "
    if not children:
        lines = make_values_lines(line_begin, node_diff, name, value, children)
    else:
        lines = make_lines_with_nodes(step, node_diff, name, value, children)
    return lines


def make_values_lines(line_begin, node_diff, name, value, children):
    value_1, value_2 = value
    lines = ''
    if node_diff is None and not children:
        lines = f'{line_begin}  {name}: {value_1}'
    elif node_diff == 'check' and not children:
        lines = f'{line_begin}- {name}: {value_1}\n'
        lines += f'{line_begin}+ {name}: {value_2}'
    elif node_diff == 'removed' and not children:
        lines = f'{line_begin}- {name}: {value_1}'
    elif node_diff == 'added' and not children:
        lines = f'{line_begin}+ {name}: {value_2}'
    return lines


def make_lines_with_nodes(step, node_diff, name, value, children):
    value_1, value_2 = value
    lines = ''
    if is_value_switch_to_node(node_diff, value_1, value_2, children):
        lines = make_value_to_node_line(step, name, value_1, children)
    elif is_node_switch_to_value(node_diff, value_1, value_2, children):
        lines = make_node_to_value_line(step, name, value_2, children)
    elif children and value_1 is None and value_2 is None:
        lines = make_nodes_line(node_diff, step, name, children)
    return lines


def is_value_switch_to_node(node_diff, value_1, value_2, children):
    if node_diff == 'check':
        if not (value_1 is None) and value_2 is None and children:
            return True
    return False


def is_node_switch_to_value(node_diff, value_1, value_2, children):
    if node_diff == 'check':
        if value_1 is None and not (value_2 is None) and children:
            return True
    return False


def make_value_to_node_line(step, name, value_1, children):
    line_begin = f"{step * '  '}  "
    lines = f'{line_begin}- {name}: {value_1}\n'
    lines += f'{line_begin}+ {name}: ' + '{\n'
    walks = list(map(lambda node: walk(node, step + 2), children))
    lines += '\n'.join(walks) + '\n'
    lines += line_begin + '  }'
    return lines


def make_node_to_value_line(step, name, value_2, children):
    line_begin = f"{step * '  '}  "
    lines = f'{line_begin}- {name}: ' + '{\n'
    walks = list(map(lambda node: walk(node, step + 2), children))
    lines += '\n'.join(walks) + '\n'
    lines += line_begin + '  }\n'
    lines += f'{line_begin}+ {name}: {value_2}'
    return lines


def make_nodes_line(node_diff, step, name, children):
    line_begin = f"{step * '  '}  "
    sign = choose_sign(node_diff)
    lines = f'{line_begin}{sign} {name}: ' + '{\n'
    walks = list(map(lambda node: walk(node, step + 2), children))
    lines += '\n'.join(walks) + '\n'
    lines += line_begin + '  }'
    return lines


def choose_sign(diff):
    if diff == 'added':
        return '+'
    if diff == 'removed':
        return '-'
    return ' '
