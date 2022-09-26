import gendiff.data


def generate_diff(file_path1, file_path2):
    data = gendiff.data.create_data(file_path1, file_path2)
    result = gendiff.data.compare_data(data)
    result = '\n'.join(result)
    print(result)
    return result
