from gendiff.data import open_file, create_tree_from_file
from gendiff.diff import create_diff
from gendiff.stylish import prepare_to_print_stylish
from gendiff.plain import prepare_to_print_plaint
from gendiff.json import prepare_to_print_json_format


def generate_diff(file_path1, file_path2, print_format='stylish'):
    file1 = open_file(file_path1)
    if file1 is None:
        return 'Wrong first file format!'
    file2 = open_file(file_path2)
    if file2 is None:
        return 'Wrong second file format!'
    file_tree1 = create_tree_from_file(file1)
    file_tree2 = create_tree_from_file(file2)
    diff = create_diff(file_tree1, file_tree2)
    if print_format == 'stylish':
        result = prepare_to_print_stylish(diff)
    elif print_format == 'plain':
        result = prepare_to_print_plaint(diff)
    elif print_format == 'json':
        result = prepare_to_print_json_format(diff)
    else:
        result = 'Wrong format!'
    return result
