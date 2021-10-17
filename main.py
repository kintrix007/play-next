#!/usr/bin/python3

import src.args as args
import sys

def main():
    parsed = args.parse_args(sys.argv[1:])
    print(str(parsed))


if __name__ == "__main__":
    main()
