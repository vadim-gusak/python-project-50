from gendiff.data import create_tree
from gendiff.diff import create_diff
from gendiff.stylish import prepare_to_print_stylish
from gendiff.plain import prepare_to_print_plaint
from gendiff.json import prepare_to_print_json_format
from gendiff.parser import parse
from os.path import isfile


def open_(path):
    if isfile(path):
        with open(path, 'r') as stream:
            text = stream.read()
    if path.endswith('.json'):
        data_format = 'json'
    elif path.endswith('.yml') or path.endswith('.yaml'):
        data_format = 'yml'
    try:
        return text, data_format
    except UnboundLocalError as e:
        print('Check file!')
        return '{}','json'


def generate_diff(path_1, path_2, print_format='stylish'):
    data_1 = parse(*open_(path_1))
    data_2 = parse(*open_(path_2))
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
