from formatter.stylish import prepare_to_print_stylish
from formatter.plain import prepare_to_print_plaint
from formatter.json import prepare_to_print_json_format


def stringify_diff(diff: list, print_format: str) -> str:
    if print_format == 'plain':
        result = prepare_to_print_plaint(diff)
    elif print_format == 'json':
        result = prepare_to_print_json_format(diff)
    elif print_format == 'stylish':
        result = prepare_to_print_stylish(diff)
    else:
        raise FileNotFoundError(f'Wrong diff format: {print_format}')
    return result
