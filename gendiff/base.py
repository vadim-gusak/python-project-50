from gendiff.diff import create_diff
from gendiff.parser import parse
from formatter.base import prepare_to_print


def open_(path):
    with open(path, 'r') as stream:
        text = stream.read()
    if path.endswith('.json'):
        data_format = 'json'
    elif path.endswith('.yml') or path.endswith('.yaml'):
        data_format = 'yml'
    else:
        data_format = ''
    return text, data_format


def generate_diff(path_1, path_2, print_format='stylish'):
    data_1 = parse(*open_(path_1))
    data_2 = parse(*open_(path_2))
    diff = create_diff(data_1, data_2)
    result = prepare_to_print(diff, print_format)
    return result
