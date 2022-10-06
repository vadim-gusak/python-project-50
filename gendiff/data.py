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


def is_end(node):
    for k, v in node.items():
        if isinstance(v, dict):
            return False
    return True


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


# def create_data(path1, path2):
#     file1 = open_file(path1)
#     file2 = open_file(path2)
#     if file1 is None or file2 is None:
#         print('Incorrect file or files!')
#         return None
#     data = {'names': []}
#     for key in file1:
#         data[key] = {'first': file1[key]}
#         data['names'].append(key)
#     for key in file2:
#         if key in data:
#             data[key]['second'] = file2[key]
#         else:
#             data[key] = {'second': file2[key]}
#             data['names'].append(key)
#     return data
#
#
# def compare_data(data):
#     result = ['{']
#     data['names'].sort()
#     for key in data['names']:
#         if 'first' in data[key] and 'second' in data[key]:
#             if data[key]['first'] == data[key]['second']:
#                 result.append(create_line(' ', key, data[key]['first']))
#             else:
#                 result.append(create_line('-', key, data[key]['first']))
#                 result.append(create_line('+', key, data[key]['second']))
#         if 'first' in data[key] and not ('second' in data[key]):
#             result.append(create_line('-', key, data[key]['first']))
#         if not ('first' in data[key]) and 'second' in data[key]:
#             result.append(create_line('+', key, data[key]['second']))
#     result.append('}')
#     return result
#
#
# def create_line(sign, name, value):
#     if isinstance(value, bool):
#         if value:
#             value = 'true'
# #         else:
#             value = 'false'
#     return f"  {sign} {name}: {value}"
