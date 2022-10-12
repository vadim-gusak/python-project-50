#!/usr/bin/env python3
import argparse
from gendiff.base import generate_diff


DESCRIPTION = 'Compares two configuration files and shows a difference.'


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("First file",
                        help='Path to json or yml file')
    parser.add_argument("Second file",
                        help='Path to second file in same format')
    parser.add_argument("-f", "--format", default='stylish',
                        help='set format of output: stylish, plain or json')
    args = parser.parse_args()
    diff = generate_diff(vars(args)['First file'],
                         vars(args)['Second file'],
                         args.format)
    print(diff)


if __name__ == '__main__':
    main()
