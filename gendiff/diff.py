def create_diff(data_1, data_2):
    names_1, names_2 = set(data_1) - set(data_2), set(data_2) - set(data_1)
    common_names = set(data_1) & set(data_2)
    result = list()
    names = list(names_1 | names_2 | common_names)
    for name in sorted(names):
        new_item = {'name': name}
        if name in names_1 or name in names_2:
            new_item['value'] = \
                data_1[name] if name in names_1 else data_2[name]
            new_item['type'] = 'removed' if name in names_1 else 'added'
            result.append(new_item)
            continue
        value_1 = data_1[name]
        value_2 = data_2[name]
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            new_item['value'] = create_diff(value_1, value_2)
            new_item['type'] = 'nested'
        elif value_1 == value_2:
            new_item['value'] = value_1
            new_item['type'] = 'unchanged'
        else:
            new_item['value'] = value_1, value_2
            new_item['type'] = 'changed'
        result.append(new_item)
    return result
