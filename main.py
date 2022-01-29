#!/usr/bin/python3

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

    assert os.path.exists(config.source_dir), f"Directory '{config.source_dir}' does not exist"
    assert os.path.exists(config.target_dir), f"Directory '{config.target_dir}' does not exist"
    
    modules = load_commands()
    for mod in modules:
        if mod.cmd_name == parsed.command.name:
            mod.run(parsed, config)
            break

if __name__ == "__main__":
    # main(); exit() #? For debugging

    try: 
        main()
    except AssertionError as e:
        msg = str(e)
        if msg != "": print(msg)
        else:         print(repr(e))

