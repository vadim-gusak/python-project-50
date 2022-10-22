import yaml
import json


def parse(data, data_format):
    if data_format == 'json':
        result = json_read(data)
    if data_format == 'yml':
        result = yml_read(data)
    try:
        return result
    except UnboundLocalError:
        print('Check data format to parse!')
        return dict()


def json_read(data):
    try:
        result = json.loads(data)
    except (json.decoder.JSONDecodeError, TypeError):
        print("Failed to read json data!")
        result = dict()
    return result


def yml_read(data):
    try:
        result = yaml.load(data, yaml.Loader)
        if isinstance(result, dict):
            return result
        else:
            return dict()
    except (AttributeError, TypeError):
        print("Failed to read yml data!")
        return dict()
