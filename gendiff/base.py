from gendiff.diff import create_diff
from gendiff.parser import parse
from formatter.base import stringify_diff


def open_(path: str) -> tuple[str, str]:
    with open(path, 'r') as stream:
        text = stream.read()
    if path.endswith('.json'):
        data_format = 'json'
    elif path.endswith('.yml') or path.endswith('.yaml'):
        data_format = 'yml'
    else:
        raise FileNotFoundError('Wrong file format!')
    return text, data_format


def generate_diff(path_1: str, path_2: str, print_format='stylish') -> str:
    ''' Compares two configuration files and return string with difference
    :param path_1: Path to the first file
    :param path_2: Path to the second file
    :param print_format: Output format: 'stylish' - default, 'plain' or 'json'
    :return: str
    '''
    data_1 = parse(*open_(path_1))
    data_2 = parse(*open_(path_2))
    diff = create_diff(data_1, data_2)
    result = stringify_diff(diff, print_format)
    return result
