from formatter.stylish import prepare_to_print_stylish
from formatter.plain import prepare_to_print_plaint
from formatter.json import prepare_to_print_json_format


def prepare_to_print(diff, print_format):
    if print_format == 'plain':
        result = prepare_to_print_plaint(diff)
    elif print_format == 'json':
        result = prepare_to_print_json_format(diff)
    else:
        result = prepare_to_print_stylish(diff)
    return result
