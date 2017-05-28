import argparse
import json
import re
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads JSON lines from standard input and prints them sorted according to one or more fields.'
                    'In particular, every line is expected to encode a shallow JSON object.'
                    'This format is sometimes called "JSON lines".'
                    'Lines with equal values in the specified fields will be sorted in the same order they were in the'
                    'input.'
    )

    parser.add_argument(
        'fields',
        type=str,
        nargs='*',
        help='Fields to be used for sorting. Every field must be in the form `<field> [asc|desc]`. If neither asc nor '
             'desc are passed, ascending order is used for the key.'
    )

    args = parser.parse_args()

    fields = []
    for field in args.fields:
        if field.endswith(' desc'):
            fields.append((field[:-5], True))
        elif field.endswith(' asc'):
            fields.append((field[:-4], True))
        else:
            fields.append((field, False))

    data = []
    for line in sys.stdin.readlines():
        try:
            info = json.loads(line)
        except json.decoder.JSONDecodeError:
            print("Line is not JSON: %s" % line, file=sys.stderr)
            sys.exit(1)

        data.append(info)

    for field, reverse in reversed(fields):
        data.sort(key=lambda entry: entry[field], reverse=reverse)

    for line in data:
        print(json.dumps(line))
