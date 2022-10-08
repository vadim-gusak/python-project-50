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
    if node['type'] == 'leaf':
        return True
    return False


def is_node(node):
    if node['type'] == 'node':
        return True
    return False


def is_switch_to_node(node):
    if node['type'] == 'to note':
        return True
    return False


def is_switch_to_leaf(node):
    if node['type'] == 'to leaf':
        return True
    return False


def get_name(node):
    return node['name']


def get_node_by_name(nodes, name):
    for item in nodes:
        if item['name'] == name:
            return item
    return None


def get_value(node):
    return node['value']


def get_second_value(node):
    return node['second value']


def get_children(node):
    return node['children']


def get_diff(node):
    return node['diff']


def add_new_value(node, value):
    node['second value'] = value
    return node


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
