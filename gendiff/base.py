from  gendiff.data import open_file, create_tree_from_file
from gendiff.diff import create_diff, prepare_to_print


def generate_diff(file_path1, file_path2):
    file1 = open_file(file_path1)
    file2 = open_file(file_path2)
    file_tree1 = create_tree_from_file(file1)
    file_tree2 = create_tree_from_file(file2)
    diff = create_diff(file_tree1, file_tree2)
    result = prepare_to_print(diff)
    print(result)
    return result
