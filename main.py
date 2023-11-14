#!/usr/bin/env python3

import sys, os
import src.args as args
from src.config import load_config
from src.cmd_loader import load_commands
from colorama import init
import src.utilz as utilz

def main():
    init(autoreset=True)
    config = load_config()
    parsed = args.parse_args(sys.argv[1:])

    assert os.path.exists(config.source_root), f"Directory '{config.source_root}' does not exist"
    assert os.path.exists(config.link_root), f"Directory '{config.link_root}' does not exist"

    modules = load_commands()
    for mod in modules:
        if mod.cmd_name == parsed.command.name:
            mod.run(parsed, config)
            break

if __name__ == "__main__":
    # TODO Change to custom errors becuase assertions are simply ignored in optiimsed mode
    # * Failing assertions should also explicitly return or throw an error

    # main(); exit() #? For debugging

    try:
        main()
    except AssertionError as e:
        msg = str(e)
        if msg != "": print("---\nError:", msg)
        else:         print(repr(e))
