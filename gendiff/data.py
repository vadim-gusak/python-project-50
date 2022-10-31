def fix_value(value):
    if isinstance(value, dict):
        return value
    elif isinstance(value, bool):
        if value:
            return 'true'
        else:
            return 'false'
    elif value is None:
        return 'null'
    return value


def get_name_type_value(item):
    name = item.get('name')
    type_ = item.get('type')
    value = item.get('value')
    return name, type_, value


def get_type(item):
    return item.get('type')


def get_name(item):
    return item.get('name')
