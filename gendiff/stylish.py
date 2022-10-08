from gendiff.data import get_name, is_leaf, get_value, get_diff, is_node
from gendiff.data import get_second_value, get_children, is_switch_to_node


def prepare_to_print_stylish(diff):
    def walk(nodes, step):
        nodes_sorted = sorted(nodes, key=get_name)
        result = []
        for item in nodes_sorted:
            if is_leaf(item):
                line = make_line_leaf(item, step)
                result.append(line)
            elif is_node(item):
                line = make_line_node(item, step)
                result.append(line)
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
            elif is_switch_to_node(item):
                line = make_line_switch_to_node(item, step)
                result.append(line)
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
            else:
                line = make_line_node(item, step)
                result.append(line)
                children = get_children(item)
                result.append(walk(children, step + 2))
                result.append(step * '  ' + '    }')
                line = make_line_switch_to_leaf(item, step)
                result.append(line)
        result = '\n'.join(result)
        return result
    return '{\n' + walk(diff, 0) + '\n}'


def fix_leaf_value(value):
    if isinstance(value, bool):
        if value:
            return str('true')
        else:
            return str('false')
    if value is None:
        return str('null')
    return str(value)


def paste_value(value):
    if value == '':
        return value
    return ' ' + value


def make_line_leaf(node, step):
    begin = f'{"  " * step}  '
    diff = get_diff(node)
    name = get_name(node)
    value = str(fix_leaf_value(get_value(node)))
    if diff is None:
        end = f'  {name}:' + paste_value(value)
    elif diff == 'added':
        end = f'+ {name}:' + paste_value(value)
    elif diff == 'removed':
        end = f'- {name}:' + paste_value(value)
    else:
        second_value = str(fix_leaf_value(get_second_value(node)))
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
    value = str(fix_leaf_value(get_value(node)))
    end = f'- {name}: {value}\n'
    end += begin + f'+ {name}: ' + '{'
    return begin + end


def make_line_switch_to_leaf(node, step):
    begin = f'{"  " * step}  '
    name = get_name(node)
    value = str(fix_leaf_value(get_value(node)))
    end = f'+ {name}: {value}'
    return begin + end
