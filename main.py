#!/usr/bin/python3

import src.args as args
from src.config import load_config
import sys

def main():
    parsed = args.parse_args(sys.argv[1:])
    config = load_config()
    print(parsed)
    print(config)


if __name__ == "__main__":
    main()
