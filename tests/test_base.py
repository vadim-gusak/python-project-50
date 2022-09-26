from gendiff.base import generate_diff


def test_generate_diff_flat():
    path1 = './tests/fixtures/test1.json'
    path2 = './tests/fixtures/test2.json'
    with open("./tests/fixtures/result1") as result_file:
        assert generate_diff(path1, path2) == result_file.read()
