import argparse
import json
import re
import sys


NUMERIC_PATTERN = re.compile(r'(\d+(?:(?:K|M|G|T|P|E)i?)?|\d+\.\d+(?:(?:K|M|G|T|P|E)i?)?)')

def float_or_int(v):
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v

def try_parse(value):
    if value.startswith('"'):
        return value[1:-1]

    if value == 'True':
        return True

    if value == 'False':
        return False

    if re.match(NUMERIC_PATTERN, value):
        if value.endswith('K'):
            return float_or_int(value[:-1]) * 1e3
        if value.endswith('M'):
            return float_or_int(value[:-1]) * 1e6
        if value.endswith('G'):
            return float_or_int(value[:-1]) * 1e9
        if value.endswith('T'):
            return float_or_int(value[:-1]) * 1e12
        if value.endswith('P'):
            return float_or_int(value[:-1]) * 1e15
        if value.endswith('E'):
            return float_or_int(value[:-1]) * 1e18
        if value.endswith('Ki'):
            return float_or_int(value[:-2]) * 1024
        if value.endswith('Mi'):
            return float_or_int(value[:-2]) * 1024 ** 2
        if value.endswith('Gi'):
            return float_or_int(value[:-2]) * 1024 ** 3
        if value.endswith('Ti'):
            return float_or_int(value[:-2]) * 1024 ** 4
        if value.endswith('Pi'):
            return float_or_int(value[:-2]) * 1024 ** 5
        if value.endswith('Ei'):
            return float_or_int(value[:-2]) * 1024 ** 6

        return float_or_int(value)

    return value


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
                    literal = try_parse(literal)
                except ValueError:
                    print("Literal not understood: %s" % literal, file=sys.stderr)
                    sys.exit(1)

                try:
                    prop_value = try_parse(info[prop])
                except ValueError:
                    print("Property not understood: %s" % info[prop], file=sys.stderr)
                    sys.exit(1)


                if operator == '==':
                    matches_condition = prop_value == literal
                elif operator == '>=':
                    matches_condition = prop_value >= literal
                elif operator == '>':
                    matches_condition = prop_value > literal
                elif operator == '<=':
                    matches_condition = prop_value <= literal
                elif operator == '<':
                    matches_condition = prop_value < literal
                elif operator == '!=':
                    matches_condition = prop_value != literal
                elif operator == '=~':
                    matches_condition = bool(re.match(literal, prop_value))
                else:
                    print("Operator not understood: %s" % operator, file=sys.stderr)
                    sys.exit(1)

                # print(operator, bool(matches_condition), literal[:10] if isinstance(literal, str) else literal, prop_value[:10] if isinstance(prop_value, str) else prop_value)
                if args.or_aggregation:
                    matches_all_conditions = matches_all_conditions or matches_condition
                else:
                    matches_all_conditions = matches_all_conditions and matches_condition

            else:
                print("Condition not understood: %s" % condition, file=sys.stderr)
                sys.exit(1)
        # print(matches_all_conditions)
        # print()
        #
        if matches_all_conditions != args.reverse:
            print(line, end='')
