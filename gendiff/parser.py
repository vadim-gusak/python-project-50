import yaml
import json
import os


def open_(path):
    if os.path.isfile(path):
        with open(path, 'r') as stream:
            text = stream.read()
    else:
        return None, None
    if path.endswith('.json'):
        data_format = 'json'
    elif path.endswith('.yml') or path.endswith('.yaml'):
        data_format = 'yml'
    else:
        return text, None
    return text, data_format


def parse(data, data_format):
    if data is None or data_format is None:
        return None
    if data_format == 'json':
        return json.loads(data)
    if data_format == 'yml':
        return yaml.load(data, yaml.Loader)
