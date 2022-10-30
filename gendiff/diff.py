from gendiff.data import fix_value


def create_diff(data_1, data_2):
    names_1, names_2 = set(data_1), set(data_2)
    common_names = names_1 & names_2
    result = list()
    for name in names_1 | names_2:
        new_item = {'name': name}
        if name in common_names:
            value_1 = fix_value(data_1[name])
            value_2 = fix_value(data_2[name])
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
            continue
        if name in names_1:
            new_item['value'] = fix_value(data_1[name])
            new_item['type'] = 'removed'
        else:
            new_item['value'] = fix_value(data_2[name])
            new_item['type'] = 'added'
        result.append(new_item)
    return result
