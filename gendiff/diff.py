from gendiff.data import fix_value


def create_diff(data_1, data_2):
    names_1, names_2 = set(data_1), set(data_2)
    common_names = names_1 & names_2
    result = list()
    for name in names_1 | names_2:
        new_item = {'name': name}
        if name in common_names:
            value_1 = fix_value(data_1[name])
            value_2 = fix_value(data_2[name])
            if isinstance(value_1, dict) and isinstance(value_2, dict):
                new_item['value'] = create_diff(value_1, value_2)
                new_item['type'] = 'nested'
            elif value_1 == value_2:
                new_item['value'] = value_1
                new_item['type'] = 'unchanged'
            else:
                new_item['value'] = value_1, value_2
                new_item['type'] = 'changed'
            result.append(new_item)
            continue
        if name in names_1:
            new_item['value'] = fix_value(data_1[name])
            new_item['type'] = 'removed'
        else:
            new_item['value'] = fix_value(data_2[name])
            new_item['type'] = 'added'
        result.append(new_item)
    return result






# import copy
# from gendiff.data import make_node, make_switch_to_leaf, make_switch_to_node
# from gendiff.data import is_node, get_node_by_name, add_second_value
# from gendiff.data import get_value, set_diff, get_children, get_name
# from gendiff.data import set_children, make_leaf
#
#
# def create_diff(nodes_1, nodes_2):
#     nodes_to_return, set_common_names = sort_nodes(nodes_1, nodes_2)
#     for name in set_common_names:
#         item_1 = get_node_by_name(nodes_1, name)
#         item_2 = get_node_by_name(nodes_2, name)
#         new_item = compare_items(name, item_1, item_2)
#         nodes_to_return.append(new_item)
#     return nodes_to_return
#
#
# def sort_nodes(nodes_1, nodes_2):
#     names_1 = set(map(lambda item: get_name(item), nodes_1))
#     names_2 = set(map(lambda item: get_name(item), nodes_2))
#     only_1st_names = names_1 - names_2
#     only_2nd_names = names_2 - names_1
#     common_names = names_1 & names_2
#     nodes_to_return = list(
#         map(
#             lambda name:
#             mark_node_diff(get_node_by_name(nodes_1, name), 'removed'),
#             only_1st_names
#         )
#     )
#     nodes_to_return += list(
#         map(
#             lambda name:
#             mark_node_diff(get_node_by_name(nodes_2, name), 'added'),
#             only_2nd_names
#         )
#     )
#     return nodes_to_return, common_names
#
#
# def mark_node_diff(original_node, mark=None):
#     node = copy.deepcopy(original_node)
#     set_diff(node, mark)
#     if is_node(node):
#         new_children = list(map(lambda item: mark_node_diff(item),
#                                 get_children(node)))
#         set_children(node, new_children)
#     return node
#
#
# def compare_items(name, item_1, item_2):
#     if item_1 == item_2:
#         return mark_node_diff(item_1)
#     elif is_node(item_1) and is_node(item_2):
#         new_children = create_diff(get_children(item_1), get_children(item_2))
#         new_item = make_node(name, new_children)
#         set_diff(new_item)
#     elif is_node(item_1):
#         new_children = list(map(mark_node_diff, get_children(item_1)))
#         value = get_value(item_2)
#         new_item = make_switch_to_leaf(name, new_children, value)
#         set_diff(new_item, 'removed')
#     elif is_node(item_2):
#         new_children = list(map(mark_node_diff, get_children(item_2)))
#         value = get_value(item_1)
#         new_item = make_switch_to_node(name, new_children, value)
#         set_diff(new_item, 'switch')
#     else:
#         value = get_value(item_1)
#         new_item = make_leaf(name, value)
#         value = get_value(item_2)
#         add_second_value(new_item, value)
#         set_diff(new_item, 'switch')
#     return new_item


# def create_diff(original_nodes_1, original_nodes_2):
#     nodes_1 = copy.deepcopy(original_nodes_1)
#     nodes_2 = copy.deepcopy(original_nodes_2)
#     not_common_nodes, set_of_common_nodes_names = sort_nodes(nodes_1, nodes_2)
#     common_nodes = []
#     for name in set_of_common_nodes_names:
#         first_item = get_node_by_name(nodes_1, name)
#         second_item = get_node_by_name(nodes_2, name)
#         if first_item == second_item:
#             common_nodes.append(mark_node_diff(first_item))
#         elif is_node(first_item) and is_node(second_item):
#             new_children = create_diff(get_children(first_item),
#                                        get_children(second_item))
#             new_item = make_node(name, new_children)
#             set_diff(new_item, None)
#             common_nodes.append(new_item)
#         elif is_node(first_item) and is_leaf(second_item):
#             new_children = list(map(mark_node_diff, get_children(first_item)))
#             new_item = make_switch_to_leaf(name,
#                                            new_children,
#                                            get_value(second_item))
#             set_diff(new_item, 'removed')
#             common_nodes.append(new_item)
#         elif is_leaf(first_item) and is_node(second_item):
#             new_children = list(map(mark_node_diff,
#                                     get_children(second_item)))
#             new_item = make_switch_to_node(name,
#                                            new_children,
#                                            get_value(first_item))
#             set_diff(new_item, 'switch')
#             common_nodes.append(new_item)
#         else:
#             value = get_value(first_item, fix_value)
#             new_item = make_leaf(name, value)
#             value = get_value(second_item, fix_value)
#             add_second_value(new_item, value)
#             set_diff(new_item, 'switch')
#             common_nodes.append(new_item)
#     return not_common_nodes + common_nodes
#
#
# def sort_nodes(nodes1, nodes2):
#     not_common_nodes = []
#     names_from_nodes1 = set([get_name(item) for item in nodes1])
#     names_from_nodes2 = set([get_name(item) for item in nodes2])
#     only_1st_names = names_from_nodes1 - names_from_nodes2
#     only_2nd_names = names_from_nodes2 - names_from_nodes1
#     common_nodes_names = names_from_nodes1 & names_from_nodes2
#     for item in nodes1 + nodes2:
#         name = get_name(item)
#         if name in only_1st_names:
#             not_common_nodes.append(mark_node_diff(item, 'removed'))
#         elif name in only_2nd_names:
#             not_common_nodes.append(mark_node_diff(item, 'added'))
#     return not_common_nodes, common_nodes_names
