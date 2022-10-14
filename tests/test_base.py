from gendiff.base import generate_diff
from pytest import mark


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
def test_generate_diff_(file_path_1, file_path_2, path_to_result):
    with open(path_to_result) as result_file:
        assert generate_diff(file_path_1, file_path_2) == result_file.read()


@mark.parametrize('file_path_1, file_path_2, print_format, path_to_result',
                  [(PATH_YML_1, PATH_YML_2, 'stylish', PATH_YAML_RESULT),
                   (PATH_JSON_1_1, PATH_JSON_1_2, 'plain',PLAIN_1_RESULT),
                   (PATH_JSON_2_1, PATH_JSON_2_2, 'plain',PLAIN_2_RESULT),
                   (PATH_JSON_1_1, PATH_JSON_1_2, 'json', JSON_FORMAT_RESULT_1),
                   (PATH_JSON_2_1, PATH_JSON_2_2, 'json', JSON_FORMAT_RESULT_2)])
def test_generate_diff(file_path_1, file_path_2, print_format, path_to_result):
    with open(path_to_result) as result_file:
        assert generate_diff(file_path_1,
                             file_path_2,
                             print_format) == result_file.read()


def test_open_file():
    wrong_file_path = './tests/fixtures/json_test_file_1_1'
    assert generate_diff(wrong_file_path, PATH_JSON_1_2) == WRONG_FILE_FORMAT_1
    assert generate_diff(PATH_JSON_1_1, wrong_file_path) == WRONG_FILE_FORMAT_2


def test_format():
    result = "Wrong format!"
    assert generate_diff(PATH_JSON_1_1, PATH_JSON_1_2, 'lol') == result
