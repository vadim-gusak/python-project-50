import yaml
import json


def parse(data, data_format):
    if data and data_format == 'json':
        result = json.loads(data)
    elif data and data_format == 'yml':
        result = yaml.load(data, yaml.Loader)
    else:
        result = {}
    return result
