from gendiff.data import get_name, is_leaf, get_value, get_diff, is_node
from gendiff.data import get_second_value, get_children, is_switch_to_node


def prepare_to_print_stylish(diff):
    def walk(nodes, step):
        nodes_sorted = sorted(nodes, key=get_name)
        result = []
        for item in nodes_sorted:
            if is_leaf(item):
                result.append(make_line_leaf(item, step))
            elif is_node(item):
                result.append(make_line_node(item, step))
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
            elif is_switch_to_node(item):
                result.append(make_line_switch_to_node(item, step))
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
            else:
                result.append(make_line_node(item, step))
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
                result.append(make_line_switch_to_leaf(item, step))
        return '\n'.join(result)
    return '{\n' + walk(diff, 0) + '\n}'


def fix_leaf_value(value):
    if isinstance(value, bool):
        if value:
            return str('true')
        else:
            return str('false')
    if value is None:
        return str('null')
    result = str(value)
    return result.strip()


def paste_value(value):
    if value == '':
        return value
    result = f' {value}'
    return result


def make_line_leaf(node, step):
    begin = f'{"  " * step}  '
    diff = get_diff(node)
    name = get_name(node)
    value = (get_value(node, fix_leaf_value))
    if diff is None:
        end = f'  {name}:' + paste_value(value)
    elif diff == 'added':
        end = f'+ {name}:' + paste_value(value)
    elif diff == 'removed':
        end = f'- {name}:' + paste_value(value)
    else:
        second_value = get_second_value(node, fix_leaf_value)
        end = f'- {name}:{paste_value(value)}\n' + begin
        end += f'+ {name}:{paste_value(second_value)}'
    return begin + end


def make_line_node(node, step):
    begin = f'{"  " * step}  '
    diff = get_diff(node)
    name = get_name(node)
    if diff is None:
        end = f'  {name}: ' + '{'
    elif diff == 'added':
        end = f'+ {name}: ' + '{'
    elif diff == 'removed':
        end = f'- {name}: ' + '{'
    return begin + end


def make_line_switch_to_node(node, step):
    begin = f'{"  " * step}  '
    name = get_name(node)
    value = get_value(node, fix_leaf_value)
    end = f'- {name}: {value}\n'
    end += begin + f'+ {name}: ' + '{'
    return begin + end


def make_line_switch_to_leaf(node, step):
    begin = f'{"  " * step}  '
    name = get_name(node)
    value = get_value(node, fix_leaf_value)
    end = f'+ {name}: {value}'
    return begin + end
