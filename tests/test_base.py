from gendiff.base import generate_diff


def test_generate_diff_flat_json():
    path1 = './tests/fixtures/json_test_flat_1.json'
    path2 = './tests/fixtures/json_test_flat_2.json'
    with open("./tests/fixtures/json_test_flat_result") as result_file:
        assert generate_diff(path1, path2) == result_file.read()


def test_generate_diff_flat_yaml():
    path1 = './tests/fixtures/yml_test_flat_1.yml'
    path2 = './tests/fixtures/yml_test_flat_2.yaml'
    with open("./tests/fixtures/yml_test_flat_result") as result_file:
        assert generate_diff(path1, path2) == result_file.read()
