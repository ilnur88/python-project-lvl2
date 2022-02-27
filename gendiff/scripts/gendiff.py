import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', metavar='first_file', type=str)
    parser.add_argument('second_file', metavar='second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(
        vars(args)['first_file'],
        vars(args)['second_file'],
        vars(args)['format'])
        )


if __name__ == '__main__':
    main()
