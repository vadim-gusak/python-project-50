from gendiff.data import get_name, is_leaf, get_value, get_diff, is_node
from gendiff.data import get_second_value, get_children, is_switch_to_node
from gendiff.data import is_switch_to_leaf


def prepare_to_print_plaint(diff):
    result = list(map(lambda item: walk(item, ''), diff))
    result = [item for item in flatten(result) if item]
    result.sort()
    result = '\n'.join(result)
    return result


def walk(node, path):
    line = ''
    path = update_path(node, path)
    if is_node(node) and get_diff(node):
        line = make_line_node_have_changes(node, path)
        return line
    if is_node(node):
        children = get_children(node)
        lines = list(map(lambda item: walk(item, path), children))
        return lines
    if is_leaf(node) and get_diff(node):
        line = make_line_leaf(node, path)
    if is_switch_to_node(node):
        line = make_line_switch_to_node(node, path)
    if is_switch_to_leaf(node):
        line = make_line_switch_to_leaf(node, path)
    return line


def update_path(node, path):
    name = get_name(node)
    if path != '':
        result = path + '.' + name
    else:
        result = name
    return result


def make_line_leaf(node, path):
    result = f"Property '{path}' was "
    diff = get_diff(node)
    value = str(fix_leaf_value(get_value(node)))
    if diff == 'added':
        result += f'added with value: {value}'
        return result
    if diff == 'removed':
        result += 'removed'
        return result
    if diff == 'switch':
        second_value = fix_leaf_value(get_second_value(node))
        result += f'updated. From {value} to {second_value}'
        return result


def make_line_switch_to_node(node, path):
    value = fix_leaf_value(get_value(node))
    result = f"Property '{path}' was updated. From {value} to [complex value]"
    return result


def make_line_switch_to_leaf(node, path):
    value = fix_leaf_value(get_value(node))
    result = f"Property '{path}' was updated. From [complex value] to {value}"
    return result


def make_line_node_have_changes(node, path):
    result = f"Property '{path}' was "
    diff = get_diff(node)
    if diff == 'added':
        result += 'added with value: [complex value]'
        return result
    if diff == 'removed':
        result += 'removed'
        return result


def fix_leaf_value(value):
    if isinstance(value, bool):
        if value:
            return str('true')
        else:
            return str('false')
    if value is None:
        return str('null')
    return "'" + str(value) + "'"


def flatten(some_list):
    result = []
    for item in some_list:
        if isinstance(item, list):
            new_items = flatten(item)
            result += new_items
        else:
            result.append(item)
    return result
