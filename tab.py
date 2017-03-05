import argparse
import json
import sys
import tabulate


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads JSON lines from standard input and tabulates given properties to standard output.'
                    'output. In particular, every line is expected to encode a shallow JSON object.'
                    'This format is sometimes called "JSON lines".'
    )


    parser.add_argument(
        'properties',
        type=str,
        nargs='*',
        help='Properties to be tabulated'
    )

    parser.add_argument(
        '--headers',
        action='store_true',
        help='If selected, headers are printed as well.'
    )

    parser.add_argument(
        '--table-format',
        type=str,
        default='plain',
        choices=[
            "plain",
            'simple',
            'grid',
            'fancy_grid',
            'pipe',
            'orgtbl',
            'jira',
            'psql',
            'rst',
            'mediawiki',
            'moinmoin',
            'html',
            'latex',
            'latex_booktabs',
            'textile'
        ],
        help='Table format. See: https://pypi.python.org/pypi/tabulate'
    )

    args = parser.parse_args()

    tabulate_lines = []
    for line in sys.stdin.readlines():
        try:
            info = json.loads(line)
        except json.decoder.JSONDecodeError:
            print("Line is not JSON: %s" % line, file=sys.stderr)
            sys.exit(1)

        tabulate_line = []
        for prop in args.properties:
            tabulate_line.append(info[prop] if prop in info else '')
        tabulate_lines.append(tabulate_line)

    if args.headers:
        print(tabulate.tabulate(tabulate_lines, headers=args.properties, tablefmt=args.table_format))
    else:
        print(tabulate.tabulate(tabulate_lines, tablefmt=args.table_format))
