import json
import yaml


def open_file(path):
    if path.endswith('.json'):
        file = json.load(open(path))
        return file
    if path.endswith('.yml') or path.endswith('.yaml'):
        with open(path, 'r') as stream:
            file = yaml.load(stream, yaml.Loader)
            print('YML File:')
            print(file)
            return file
    print('Incorrect file or files!')
    return None


def create_data(path1, path2):
    file1 = open_file(path1)
    file2 = open_file(path2)
    data = {'names': []}
    for key in file1:
        data[key] = {'first': file1[key]}
        data['names'].append(key)
    for key in file2:
        if key in data:
            data[key]['second'] = file2[key]
        else:
            data[key] = {'second': file2[key]}
            data['names'].append(key)
    return data


def compare_data(data):
    result = ['{']
    data['names'].sort()
    for key in data['names']:
        if 'first' in data[key] and 'second' in data[key]:
            if data[key]['first'] == data[key]['second']:
                result.append(create_line(' ', key, data[key]['first']))
            else:
                result.append(create_line('-', key, data[key]['first']))
                result.append(create_line('+', key, data[key]['second']))
        if 'first' in data[key] and not ('second' in data[key]):
            result.append(create_line('-', key, data[key]['first']))
        if not ('first' in data[key]) and 'second' in data[key]:
            result.append(create_line('+', key, data[key]['second']))
    result.append('}')
    return result


def create_line(sign, name, value):
    if isinstance(value, bool):
        if value:
            value = 'true'
        else:
            value = 'false'
    return f"  {sign} {name}: {value}"
