#!/usr/bin/python3

import sys, os
import src.args as args
from src.config import load_config
from src.cmd_loader import load_commands
import colorama
import src.utilz as utilz

def main():
    # Makes colorama actually work
    colorama.init(autoreset=True)
    
    parsed = args.parse_args(sys.argv[1:])
    config = load_config()
    # print(os.environ.get("PLAY_NEXT_EP_MASTER_DIR"))

    if not os.path.exists(config.source_root):
        raise FileNotFoundError(f"Directory '{config.source_root}' does not exist")
    if not os.path.exists(config.link_root):
        raise FileNotFoundError(f"Directory '{config.link_root}' does not exist")

    modules = load_commands()
    for mod in modules:
        if mod.cmd_name == parsed.command.name:
            mod.run(parsed, config)
            break

if __name__ == "__main__":
    # TODO Change to custom errors becuase assertions are simply ignored in optiimsed mode
    # * Failing assertions should also explicitly return or throw an error

    main(); exit() #? For debugging

    try:
        main()
    except AssertionError as e:
        msg = str(e)
        if msg != "": print("---\nError:", msg)
        else:         print(repr(e))
