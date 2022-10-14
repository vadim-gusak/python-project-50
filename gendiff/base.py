from gendiff.data import create_tree
from gendiff.diff import create_diff
from gendiff.stylish import prepare_to_print_stylish
from gendiff.plain import prepare_to_print_plaint
from gendiff.json import prepare_to_print_json_format


def generate_diff(data_1, data_2, print_format='stylish'):
    tree_1 = create_tree(data_1)
    tree_2 = create_tree(data_2)
    diff = create_diff(tree_1, tree_2)
    if print_format == 'plain':
        result = prepare_to_print_plaint(diff)
    elif print_format == 'json':
        result = prepare_to_print_json_format(diff)
    else:
        result = prepare_to_print_stylish(diff)
    return result
