import json
import yaml
import copy


def open_file(path):
    if path.endswith('.json'):
        with open(path, 'r') as stream:
            file = json.load(stream)
            return file
    if path.endswith('.yml') or path.endswith('.yaml'):
        with open(path, 'r') as stream:
            file = yaml.load(stream, yaml.Loader)
            return file
    return None


def make_leaf(name, value):
    value = fix_value(value)
    result = {'name': name, 'value': value, 'type': 'leaf'}
    return result


def make_node(name, children):
    result = {'name': name, 'type': 'node', 'children': children}
    return result


def make_switch_to_leaf(name, children, value):
    result = {'name': name, 'type': 'to leaf',
              'children': children, 'value': value}
    return result


def make_switch_to_node(name, children, value):
    result = {'name': name, 'type': 'to node',
              'children': children, 'value': value}
    return result


def is_end(node):
    for k, v in node.items():
        if isinstance(v, dict):
            return False
    return True


def is_leaf(node):
    if node.get('type') == 'leaf':
        return True
    return False


def is_node(node):
    if node.get('type') == 'node':
        return True
    return False


def is_switch_to_node(node):
    if node.get('type') == 'to node':
        return True
    return False


def is_switch_to_leaf(node):
    if node.get('type') == 'to leaf':
        return True
    return False


def get_name(node):
    return node.get('name')


def get_node_by_name(nodes, name):
    for item in nodes:
        if item.get('name') == name:
            return item
    return None


def get_value(node, func_to_fix_value=lambda v: v):
    return func_to_fix_value(node.get('value'))


def get_second_value(node, func_to_fix_value=lambda v: v):
    return func_to_fix_value(node.get('second value'))


def get_children(node):
    return node.get('children')


def get_diff(node):
    return node.get('diff')


def get_type(node):
    return node.get('type')


def add_second_value(node, value):
    node['second value'] = value


def set_diff(node, diff):
    node['diff'] = diff


def set_children(node, children):
    node['children'] = children


def fix_value(value):
    # if isinstance(value, bool) or value is None:
    #     return value
    if isinstance(value, str):
        return value.strip()
    return value


def create_tree_from_file(node):
    node_copy = copy.deepcopy(node)
    leafs = [make_leaf(key, value)
             for key, value in node_copy.items()
             if not isinstance(value, dict)]
    if is_end(node_copy):
        return leafs
    nodes = []
    for key, value in node_copy.items():
        if isinstance(value, dict):
            children = create_tree_from_file(value)
            nodes.append(make_node(key, children))
    return leafs + nodes
