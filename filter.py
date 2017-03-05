import argparse
import json
import re
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads JSON lines from standard input and prints those (not) matching given conditions to standard'
                    'output. In particular, every line is expected to encode a shallow JSON object.'
                    'This format is sometimes called "JSON lines".'
    )

    parser.add_argument(
        '-r',
        '--reverse',
        action='store_true',
        help='If selected, entries matching the conditions will NOT be output and those not matching WILL BE output.'
    )

    parser.add_argument(
        '--or',
        dest='or_aggregation',
        action='store_true',
        help='If selected, conditions will be aggregated using logical OR; otherwise, logical AND will be used.'
    )

    parser.add_argument(
        'conditions',
        type=str,
        nargs='*',
        help='Conditions to be verified. Every condition must be in the form `<property> <operator> <literal>`.'
             'Operators can be any of ==, >=, >, <=, < !=, =~.'
             'Literals can be:'
             ' - strings like "abc"'
             ' - numbers like 2, 3.14, 1e03, 15K (15*1000) or 23Ki (23 * 1024)'
             ' - booleans like True or False'
             ' - regular expressions like "a\d+$"'
    )

    args = parser.parse_args()
    pattern = re.compile(r'([a-zA-Z0-9-_]+) *(==|>=|>|<=|<|!=|=~) *(\d+(?:(?:K|M|G|T|P|E)i?)?|\d+\.\d+(?:(?:K|M|G|T|P|E)i?)?|\d+\.\d+e\d+|"[^"]+"|True|False)')

    for line in sys.stdin.readlines():
        try:
            info = json.loads(line)
        except json.decoder.JSONDecodeError:
            print("Line is not JSON: %s" % line, file=sys.stderr)
            sys.exit(1)

        matches_all_conditions = False if args.or_aggregation else True
        for condition in args.conditions:
            match = re.match(pattern, condition)
            if match:
                prop = match.group(1)
                operator = match.group(2)
                literal = match.group(3)

                if prop not in info:
                    print("Property not found: %s" % prop, file=sys.stderr)
                    sys.exit(1)

                try:
                    if literal.startswith('"'):
                        pass
                    elif literal == 'True':
                        literal = True
                    elif literal == 'False':
                        literal = False
                    elif literal.endswith('K'):
                        literal = float(literal[:-1]) * 1e3
                    elif literal.endswith('M'):
                        literal = float(literal[:-1]) * 1e6
                    elif literal.endswith('G'):
                        literal = float(literal[:-1]) * 1e9
                    elif literal.endswith('T'):
                        literal = float(literal[:-1]) * 1e12
                    elif literal.endswith('P'):
                        literal = float(literal[:-1]) * 1e15
                    elif literal.endswith('E'):
                        literal = float(literal[:-1]) * 1e18
                    elif literal.endswith('Ki'):
                        literal = float(literal[:-2]) * 1024
                    elif literal.endswith('Mi'):
                        literal = float(literal[:-2]) * 1024**2
                    elif literal.endswith('Gi'):
                        literal = float(literal[:-2]) * 1024**3
                    elif literal.endswith('Ti'):
                        literal = float(literal[:-2]) * 1024**4
                    elif literal.endswith('Pi'):
                        literal = float(literal[:-2]) * 1024**5
                    elif literal.endswith('Ei'):
                        literal = float(literal[:-2]) * 1024**6
                    else:
                        literal = float(literal)
                except ValueError:
                    print("Literal not understood: %s" % literal, file=sys.stderr)
                    sys.exit(1)


                if operator == '==':
                    matches_condition = info[prop] == literal
                elif operator == '>=':
                    matches_condition = info[prop] >= literal
                elif operator == '>':
                    matches_condition = info[prop] > literal
                elif operator == '<=':
                    matches_condition = info[prop] <= literal
                elif operator == '<':
                    matches_condition = info[prop] < literal
                elif operator == '!=':
                    matches_condition = info[prop] != literal
                elif operator == '=~':
                    matches_condition = re.match(literal, info[prop])
                else:
                    print("Operator not understood: %s" % operator, file=sys.stderr)
                    sys.exit(1)

                if args.or_aggregation:
                    matches_all_conditions = matches_all_conditions or matches_condition
                else:
                    matches_all_conditions = matches_all_conditions and matches_condition

            else:
                print("Condition not understood: %s" % condition, file=sys.stderr)
                sys.exit(1)

        if matches_all_conditions != args.reverse:
            print(line, end='')
