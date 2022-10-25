from gendiff.data import get_name, get_node_by_name, get_value, get_children
from gendiff.data import is_node, make_node, set_value, set_value_deep
from gendiff.data import set_diff, set_diff_deep


def create_diff(tree_1, tree_2):
    diff = []
    names_1 = set(map(lambda item: get_name(item), tree_1))
    names_2 = set(map(lambda item: get_name(item), tree_2))
    common_names = names_1 & names_2
    names_1 = names_1 - common_names
    names_2 = names_2 - common_names
    for name in names_1:
        new_item = get_node_by_name(tree_1, name).copy()
        set_value_deep(new_item, (get_value(new_item), None))
        set_diff_deep(new_item, None)
        set_diff(new_item, 'removed')
        diff.append(new_item)
    for name in names_2:
        new_item = get_node_by_name(tree_2, name).copy()
        set_value_deep(new_item, (None, get_value(new_item)))
        set_diff_deep(new_item, None)
        set_diff(new_item, 'added')
        diff.append(new_item)
    for name in common_names:
        item_1 = get_node_by_name(tree_1, name).copy()
        item_2 = get_node_by_name(tree_2, name).copy()
        children_1, children_2 = get_children(item_1), get_children(item_2)
        value_1, value_2 = get_value(item_1), get_value(item_2)
        if item_1 == item_2:
            new_item = item_1.copy()
            set_diff_deep(new_item, None)
            set_value_deep(new_item, (value_1, value_2))
            diff.append(new_item)
            continue
        if is_node(item_1) and is_node(item_2):
            new_children = create_diff(children_1, children_2)
            new_item = make_node(name, new_children)
            set_value(new_item, (None, None))
            set_diff(new_item, None)
            diff.append(new_item)
        else:
            children = children_1 + children_2
            new_children = create_diff(children, children)
            new_item = make_node(name, new_children)
            set_diff_deep(new_item, None)
            set_diff(new_item, 'check')
            set_value(new_item, (value_1, value_2))
            diff.append(new_item)
    return diff
