import argparse
import json
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads JSON lines from standard input and prints a sorted list of all the (unique) keys available.'
    )
    parser.add_argument(
        '--sep',
        type=str,
        default=' ',
        help='Separator for list elements'
    )

    args = parser.parse_args()

    all_keys = set()
    for line in sys.stdin.readlines():
        try:
            info = json.loads(line)
        except json.decoder.JSONDecodeError:
            print("Line is not JSON: %s" % line, file=sys.stderr)
            sys.exit(1)
        all_keys |= set(info)
    print(args.sep.join(sorted(all_keys)))
