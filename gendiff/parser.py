import yaml
import json


def parse(data: str, data_format: str) -> dict:
    if data and data_format == 'json':
        return json.loads(data)
    elif data and data_format == 'yml':
        return yaml.load(data, yaml.Loader)
    else:
        raise FileNotFoundError(f"Wrong data_format: {data_format}")
