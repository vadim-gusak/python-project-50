import copy


def is_leaf(node):
    if node['type'] == 'leaf':
        return True
    return False


def is_node(node):
    if node['type'] == 'node':
        return True
    return False


def sort_names(node1, node2):
    names1 = [v['name'] for v in node1]
    names2 = [v['name'] for v in node2]
    equal_names = []
    names1_only = []
    names2_only = []
    for name in names1:
        if name in names2:
            equal_names.append(name)
        else:
            names1_only.append(name)
    for name in names2:
        if not(name in names1):
            names2_only.append(name)
    return names1_only, names2_only, equal_names


def create_diff(original_node1, original_node2):
    node1 = copy.deepcopy(original_node1)
    node2 = copy.deepcopy(original_node2)
    diff = []
    names_in_1st_node, names_in_2nd_node, equal_names = sort_names(node1,
                                                                   node2)
    for node1_item in node1:
        if node1_item['name'] in names_in_1st_node:
            node1_item['diff'] = '-'
            diff.append(node1_item)
            continue
        for node2_item in node2:
            if node2_item['name'] == node1_item['name']:
                if node1_item == node2_item:
                    node1_item['diff'] = None
                    diff.append(node1_item)
                elif is_node(node1_item) and is_node(node2_item):
                    children = create_diff(node1_item['children'],
                                           node2_item['children'])
                    node1_item['children'] = children
                    node1_item['diff'] = None
                    diff.append(node1_item)
                else:
                    node1_item['diff'] = '-'
                    diff.append(node1_item)
                    node2_item['diff'] = '+'
                    diff.append(node2_item)
                break
    for node2_item in node2:
        if node2_item['name'] in names_in_2nd_node:
            node2_item['diff'] = '+'
            diff.append(node2_item)
    return diff


def prepare_to_print(diff):
    def walk(original_node, step):
        node = copy.deepcopy(original_node)
        node_sorted = sorted(node, key=get_name)
        result= []
        for item in node_sorted:
            if not ('diff' in item):
                item['diff'] = None
            if is_leaf(item):
                item['value'] = fix_leaf_value(item['value'])
                result.append(make_line(item, step) + str(item['value']))
            else:
                result.append(make_line(item, step) + ' {')
                result.append(walk(item['children'], step + 2))
                result.append(step * '  ' + '    }')
        result = '\n'.join(result)
        return result
    return '{\n' + walk(diff, 0) + '\n}'


def get_name(node):
    return node['name']


def fix_leaf_value(value):
    if isinstance(value, bool):
        if value:
            return str('true')
        else:
            return str('false')
    if value is None:
        return str('null')
    return str(value)


def make_line(node, step):
    result = f'{"  " * step}  '
    if not node['diff'] is None:
        result += f"{node['diff']} "
    else:
        result += '  '
    result += f"{node['name']}:"
    if is_leaf(node) and node['value'] != '':
        result += ' '
    return result