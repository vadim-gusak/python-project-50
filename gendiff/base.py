from os.path import isfile
from gendiff.diff import create_diff
from gendiff.parser import parse
from formatter.plain import prepare_to_print_plaint
from formatter.stylish import prepare_to_print_stylish
from formatter.json import prepare_to_print_json_format


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
    except UnboundLocalError:
        print('Check file!')
        return '{}', 'json'


def generate_diff(path_1, path_2, print_format='stylish'):
    data_1 = parse(*open_(path_1))
    data_2 = parse(*open_(path_2))
    diff = create_diff(data_1, data_2)
    if print_format == 'plain':
        result = prepare_to_print_plaint(diff)
    elif print_format == 'json':
        result = prepare_to_print_json_format(diff)
    else:
        result = prepare_to_print_stylish(diff)
    return result
