from gendiff.base import generate_diff, open_
from gendiff.parser import parse
from gendiff.diff import create_diff
from formatter.stylish import prepare_to_print_stylish
from formatter.plain import prepare_to_print_plaint
from formatter.json import prepare_to_print_json_format
from formatter.base import stringify_diff
import pytest
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


@pytest.mark.parametrize('file_path_1, file_path_2, path_to_result',
                         [(PATH_JSON_FLAT_1, PATH_JSON_FLAT_2, PATH_JSON_FLAT_RESULT),
                          (PATH_YML_FLAT_1, PATH_YML_FLAT_2, PATH_YML_FLAT_RESULT),
                          (PATH_JSON_1_1, PATH_JSON_1_2, PATH_JSON_1_RESULT),
                          (PATH_JSON_2_1, PATH_JSON_2_2, PATH_JSON_2_RESULT)])
def test_generate_diff(file_path_1, file_path_2, path_to_result):
    with open(path_to_result) as result_file:
        assert generate_diff(file_path_1, file_path_2) == result_file.read()


@pytest.mark.parametrize('file_path_1, file_path_2, print_format, path_to_result',
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


def test_open_raises_exception():
    with pytest.raises(FileNotFoundError):
        open_(PATH_JSON_FLAT_RESULT)


def test_parse_raises_exception():
    with pytest.raises(FileNotFoundError):
        parse('something', 'wrong format')


def test_stringify_diff_raises_exception():
    with pytest.raises(FileNotFoundError):
        stringify_diff('diff data', 'wrong format')


def test_create_diff_is_clear():
    data_1 = parse(*open_(PATH_JSON_1_1))
    data_1_copy = copy.deepcopy(data_1)
    data_2 = parse(*open_(PATH_JSON_1_2))
    data_2_copy = copy.deepcopy(data_2)
    create_diff(data_1, data_2)
    assert data_1 == data_1_copy
    assert data_2 == data_2_copy


def test_prepare_to_print_is_clear():
    data_1 = parse(*open_(PATH_JSON_1_1))
    data_2 = parse(*open_(PATH_JSON_1_2))
    diff = create_diff(data_1, data_2)
    diff_copy = copy.deepcopy(diff)
    prepare_to_print_stylish(diff)
    prepare_to_print_plaint(diff)
    prepare_to_print_json_format(diff)
    assert diff == diff_copy
