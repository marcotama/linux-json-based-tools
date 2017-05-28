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
    pattern = re.compile(r'(.+) *(asc|desc)?')

    fields = []
    for field in args.fields:
        match = re.match(pattern, field)
        if match:
            f, rev = match.groups()
            if rev == 'desc':
                rev = True
            else:
                rev = False
            fields.append((f, rev))

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
