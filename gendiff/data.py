def get_name_type_value(item: dict) -> tuple[str, str, str]:
    name = item.get('name')
    type_ = item.get('type')
    value = item.get('value')
    return name, type_, value


def get_children(item: dict) -> list:
    return item.get('children')
