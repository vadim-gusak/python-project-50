from gendiff.base import generate_diff, open_
from gendiff.parser import parse
from gendiff.data import create_tree
from gendiff.diff import create_diff
from pytest import mark
import copy


PATH_JSON_FLAT_1 = './tests/fixtures/json_test_flat_1.json'
PATH_JSON_FLAT_2 = './tests/fixtures/json_test_flat_2.json'
PATH_JSON_FLAT_RESULT = './tests/fixtures/json_test_flat_result'
PATH_YML_FLAT_1 = './tests/fixtures/yml_test_flat_1.yml'
PATH_YML_FLAT_2 = './tests/fixtures/yml_test_flat_2.yaml'
PATH_YML_FLAT_RESULT = './tests/fixtures/yml_test_flat_result'
PATH_JSON_1_1 = './tests/fixtures/json_test_file_1_1.json'
PATH_JSON_1_2 = './tests/fixtures/json_test_file_1_2.json'
PATH_JSON_1_RESULT = './tests/fixtures/json_test_file_1_result'
PATH_JSON_2_1 = './tests/fixtures/json_test_file_2_1.json'
PATH_JSON_2_2 = './tests/fixtures/json_test_file_2_2.json'
PATH_JSON_2_RESULT = './tests/fixtures/json_test_file_2_result'
PATH_YML_1 = './tests/fixtures/yml_test_1_1.yml'
PATH_YML_2 = './tests/fixtures/yml_test_1_2.yaml'
PATH_YAML_RESULT = './tests/fixtures/json_test_file_1_result'
PLAIN_1_RESULT = './tests/fixtures/plain_1_result'
PLAIN_2_RESULT = './tests/fixtures/plain_2_result'
JSON_FORMAT_RESULT_1 = './tests/fixtures/json_format_result_1.json'
JSON_FORMAT_RESULT_2 = './tests/fixtures/json_format_result_2.json'
WRONG_FILE_FORMAT_1 = 'Wrong first file format!'
WRONG_FILE_FORMAT_2 = 'Wrong second file format!'


@mark.parametrize('file_path_1, file_path_2, path_to_result',
                  [(PATH_JSON_FLAT_1, PATH_JSON_FLAT_2, PATH_JSON_FLAT_RESULT),
                   (PATH_YML_FLAT_1, PATH_YML_FLAT_2, PATH_YML_FLAT_RESULT),
                   (PATH_JSON_1_1, PATH_JSON_1_2, PATH_JSON_1_RESULT),
                   (PATH_JSON_2_1, PATH_JSON_2_2, PATH_JSON_2_RESULT)])
def test_generate_diff(file_path_1, file_path_2, path_to_result):
    with open(path_to_result) as result_file:
        assert generate_diff(file_path_1, file_path_2) == result_file.read()


@mark.parametrize('file_path_1, file_path_2, print_format, path_to_result',
                  [(PATH_YML_1, PATH_YML_2, 'stylish', PATH_YAML_RESULT),
                   (PATH_YML_1, PATH_YML_2, 'plain', PLAIN_1_RESULT),
                   (PATH_YML_1, PATH_YML_2, 'json', JSON_FORMAT_RESULT_1),
                   (PATH_JSON_1_1, PATH_JSON_1_2, 'plain', PLAIN_1_RESULT),
                   (PATH_JSON_2_1, PATH_JSON_2_2, 'plain', PLAIN_2_RESULT),
                   (PATH_JSON_1_1, PATH_JSON_1_2, 'json', JSON_FORMAT_RESULT_1),
                   (PATH_JSON_2_1, PATH_JSON_2_2, 'json', JSON_FORMAT_RESULT_2)])
def test_generate_diff_format(file_path_1, file_path_2, print_format, path_to_result):
    with open(path_to_result) as result_file:
        assert generate_diff(file_path_1,
                             file_path_2,
                             print_format) == result_file.read()


def test_parse():
    res = dict()
    assert parse(*open_(PATH_JSON_1_RESULT)) == res
    assert parse(*open_('https://ru.hexlet.io')) == res
    assert parse('any text data', 'wrong format') == res
    assert parse(None, 'yml') == res
    assert parse(None, 'json') == res
    assert parse(None, None) == res
    assert parse('some not yml text data', 'yml') == res
    assert parse('some not json text data', 'json') == res


def test_create_diff_clear():
    data_1 = parse(*open_(PATH_JSON_1_1))
    tree_1 = create_tree(data_1)
    tree_1_copy = copy.deepcopy(tree_1)
    data_2 = parse(*open_(PATH_JSON_1_2))
    tree_2 = create_tree(data_2)
    tree_2_copy = copy.deepcopy(tree_2)
    diff = create_diff(tree_1, tree_2)
    assert tree_1 == tree_1_copy
    assert tree_2 == tree_2_copy

