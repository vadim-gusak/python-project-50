#!/usr/bin/env python3
import argparse
from gendiff.base import generate_diff


DESCRIPTION = 'Compares two configuration files and shows a difference.'


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("first_file",
                        help='Path to json or yml file')
    parser.add_argument("second_file",
                        help='Path to second file in same format')
    parser.add_argument("-f", "--format", default='stylish',
                        help='set format of output: stylish, plain or json')
    return parser.parse_args()


def main():
    args = parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main__':
    main()
