from gendiff.base import generate_diff


def test_generate_diff_flat_json():
    path1 = './tests/fixtures/json_test_flat_1.json'
    path2 = './tests/fixtures/json_test_flat_2.json'
    with open("./tests/fixtures/json_test_flat_result") as result_file:
        assert generate_diff(path1, path2, 'stylish') == result_file.read()


def test_generate_diff_flat_yaml():
    path1 = './tests/fixtures/yml_test_flat_1.yml'
    path2 = './tests/fixtures/yml_test_flat_2.yaml'
    with open("./tests/fixtures/yml_test_flat_result") as result_file:
        assert generate_diff(path1, path2, 'stylish') == result_file.read()


def test_generate_diff_json_standart():
    path1 = './tests/fixtures/json_test_file_1_1.json'
    path2 = './tests/fixtures/json_test_file_1_2.json'
    with open('./tests/fixtures/json_test_file_1_result') as result_file:
        assert generate_diff(path1, path2, 'stylish') == result_file.read()


def test_generate_diff_json_standart_2():
    path1 = './tests/fixtures/json_test_file_2_1.json'
    path2 = './tests/fixtures/json_test_file_2_2.json'
    with open('./tests/fixtures/json_test_file_2_result') as result_file:
        assert generate_diff(path1, path2, 'stylish') == result_file.read()


def test_generate_diff_yml_standart():
    path1 = './tests/fixtures/yml_test_1_1.yml'
    path2 = './tests/fixtures/yml_test_1_2.yaml'
    with open('./tests/fixtures/json_test_file_1_result') as result_file:
        assert generate_diff(path1, path2, 'stylish') == result_file.read()


def test_generate_diff_plain_2():
    path1 = './tests/fixtures/json_test_file_2_1.json'
    path2 = './tests/fixtures/json_test_file_2_2.json'
    with open('./tests/fixtures/plain_2_result') as result_file:
        assert generate_diff(path1, path2, 'plain') == result_file.read()


def test_generate_diff_plain():
    path1 = './tests/fixtures/json_test_file_1_1.json'
    path2 = './tests/fixtures/json_test_file_1_2.json'
    with open('./tests/fixtures/plain_1_result') as result_file:
        assert generate_diff(path1, path2, 'plain') == result_file.read()


def test_open_file1():
    path1 = './tests/fixtures/json_test_file_1_1'
    path2 = './tests/fixtures/json_test_file_1_2.json'
    result = 'Wrong first file format!'
    assert generate_diff(path1, path2) == result
    path1 = './tests/fixtures/json_test_file_1_1.json'
    path2 = './tests/fixtures/json_test_file_1_2'
    result = 'Wrong second file format!'
    assert generate_diff(path1, path2) == result


def test_format():
    result = "Wrong format!"
    path1 = './tests/fixtures/json_test_file_1_1.json'
    path2 = './tests/fixtures/json_test_file_1_2.json'
    assert generate_diff(path1, path2, 'lol') == result

