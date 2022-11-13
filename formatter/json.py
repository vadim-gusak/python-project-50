from json import dumps


def prepare_to_print_json_format(diff):
    return dumps(diff, sort_keys=True, indent=2)
