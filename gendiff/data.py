def get_name_type_value(item):
    name = item.get('name')
    type_ = item.get('type')
    value = item.get('value')
    return name, type_, value


def get_name(item):
    return item.get('name')
