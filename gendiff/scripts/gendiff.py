import argparse

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('string', metavar='first_file')
parser.add_argument('string', metavar='second_file')
parser.add_argument('-f', '--format', help='set format of output')
args = parser.parse_args()

