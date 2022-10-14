#!/usr/bin/env python3
import argparse
from gendiff.parser import open_, parse
from gendiff.base import generate_diff


DESCRIPTION = 'Compares two configuration files and shows a difference.'


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("first_file",
                        help='Path to json or yml file')
    parser.add_argument("second_file",
                        help='Path to second file in same format')
    parser.add_argument("-f", "--format", default='stylish',
                        choices=['stylish', 'plain', 'json'],
                        help='set format of output: stylish, plain or json')
    return parser.parse_args()


def main():
    args = parse_args()
    data_1 = parse(*open_(args.first_file))
    data_2 = parse(*open_(args.second_file))
    if data_1 is None or data_2 is None:
        print('Incorrect input data!')
        return
    diff = generate_diff(data_1, data_2, args.format)
    print(diff)


if __name__ == '__main__':
    main()
