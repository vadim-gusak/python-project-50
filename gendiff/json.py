from gendiff.data import get_name, is_node, get_children, is_switch_to_node
from gendiff.data import is_leaf, get_value, get_diff, get_type
from gendiff.data import get_second_value


def prepare_to_print_json_format(diff):
    return '{\n' + walk(diff, 0) + '\n}'


def walk(nodes, step):
    nodes_sorted = sorted(nodes, key=get_name)
    result = []
    for index, item in enumerate(nodes_sorted):
        if is_leaf(item):
            result.append(make_line_leaf(item, step))
        elif is_node(item):
            result.append(make_line_node(item, step))
            children = get_children(item)
            result.append(walk(children, step + 1))
            result.append(step * '  ' + '  }')
        elif is_switch_to_node(item):
            result.append(make_line_leaf(item, step) + ',')
            result.append(make_line_node(item, step))
            children = get_children(item)
            result.append(walk(children, step + 1))
            result.append(step * '  ' + '  }')
        else:
            result.append(make_line_node(item, step))
            children = get_children(item)
            result.append(walk(children, step + 1))
            result.append(step * '  ' + '  },')
            result.append(make_line_leaf(item, step))
        if index < len(nodes_sorted) - 1:
            result[len(result) - 1] += ','
    return '\n'.join(result)


def make_line_leaf(node, step):
    name = get_name(node)
    value = get_value(node, fix_leaf_value)
    base_line = f'{step * "  "}{"  "}"{name}": {value}'
    diff = get_diff(node)
    if diff == 'added':
        result = f'{step * "  "}{"  "}"{name}_added": {value}'
        return result
    if diff == 'removed':
        if node.get('type') == 'to leaf':
            return f'{step * "  "}{"  "}"{name}_updated": {value}'
        result = f'{step * "  "}{"  "}"{name}_removed": {value}'
        return result
    if diff == 'switch':
        if get_type(node) == 'to node':
            return base_line
        result = [base_line + ',']
        second_value = get_second_value(node, fix_leaf_value)
        result.append(f'{step * "  "}{"  "}"{name}_updated": {second_value}')
        result = '\n'.join(result)
        return result
    return base_line


def make_line_node(node, step):
    name = get_name(node)
    diff = get_diff(node)
    if get_type(node) == 'to leaf':
        return f'{step * "  "}{"  "}"{name}": ' + '{'
    if diff == 'removed':
        name += '_removed'
    if diff == 'switch':
        name += '_updated'
    if diff == 'added':
        name += '_added'
    result = f'{step * "  "}{"  "}"{name}": ' + '{'
    return result


def fix_leaf_value(value):
    if isinstance(value, bool):
        if value:
            return str('true')
        else:
            return str('false')
    if value is None:
        return str('null')
    if isinstance(value, str):
        return '"' + value + '"'
    return str(value)
