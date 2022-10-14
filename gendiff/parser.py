import yaml
import json


def parse(data, data_format):
    if data is None or data_format is None:
        return None
    if data_format == 'json':
        return json.loads(data)
    if data_format == 'yml':
        return yaml.load(data, yaml.Loader)
