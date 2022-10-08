import copy
from gendiff.data import make_node, make_switch_to_leaf, make_switch_to_node
from gendiff.data import is_leaf, is_node, get_node_by_name, add_new_value
from gendiff.data import get_value


def create_diff(original_nodes_1, original_nodes_2):
    nodes_1 = copy.deepcopy(original_nodes_1)
    nodes_2 = copy.deepcopy(original_nodes_2)
    not_common_nodes, set_of_common_nodes_names = sort_nodes(nodes_1, nodes_2)
    common_nodes = []
    for name in set_of_common_nodes_names:
        first_item = get_node_by_name(nodes_1, name)
        second_item = get_node_by_name(nodes_2, name)
        if first_item == second_item:
            common_nodes.append(mark_node_diff(first_item))
        elif is_node(first_item) and is_node(second_item):
            new_children = create_diff(first_item['children'],
                                       second_item['children'])
            new_item = make_node(name, new_children)
            new_item['diff'] = None
            common_nodes.append(new_item)
        elif is_node(first_item) and is_leaf(second_item):
            new_children = list(map(mark_node_diff, first_item['children']))
            new_item = make_switch_to_leaf(name,
                                           new_children,
                                           second_item['value'])
            new_item['diff'] = 'removed'
            common_nodes.append(new_item)
        elif is_leaf(first_item) and is_node(second_item):
            new_children = list(map(mark_node_diff, second_item['children']))
            new_item = make_switch_to_node(name,
                                           new_children,
                                           first_item['value'])
            new_item['diff'] = 'switch'
            common_nodes.append(new_item)
        else:
            value = get_value(second_item)
            new_item = add_new_value(first_item, value)
            new_item['diff'] = 'switch'
            common_nodes.append(new_item)
    return not_common_nodes + common_nodes


def sort_nodes(nodes1, nodes2):
    not_common_nodes = []
    names_from_nodes1 = set([item['name'] for item in nodes1])
    names_from_nodes2 = set([item['name'] for item in nodes2])
    only_1st_names = names_from_nodes1 - names_from_nodes2
    only_2nd_names = names_from_nodes2 - names_from_nodes1
    common_nodes_names = names_from_nodes1 & names_from_nodes2
    nodes = nodes1 + nodes2
    for item in nodes:
        if item['name'] in only_1st_names:
            not_common_nodes.append(mark_node_diff(item, 'removed'))
        elif item['name'] in only_2nd_names:
            not_common_nodes.append(mark_node_diff(item, 'added'))
    return not_common_nodes, common_nodes_names


def mark_node_diff(original_node, mark=None):
    node = copy.deepcopy(original_node)
    node['diff'] = mark
    if is_node(node):
        node['children'] = list(map(lambda item: mark_node_diff(item),
                                    node['children']))
    return node
