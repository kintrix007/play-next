from src.config import Config
from src.arg_data import COMMANDS, ParsedArgs
from importlib import import_module

COMMAND_ROOT = "src.commands"

class CmdTemplate:
    cmd_name = "create"

    def run(self, parsed: ParsedArgs, config: Config) -> None:
        raise NotImplementedError()


def load_commands() -> list[CmdTemplate]:
    modules = [import_module(f"{COMMAND_ROOT}.{cmd}") for cmd in COMMANDS.keys()]
    return modules
