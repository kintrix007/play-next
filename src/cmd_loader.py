from ast import Call
from src.config import Config
from src.arg_data import COMMANDS
from src.command_line_argument import ParsedArgs
from importlib import import_module

COMMAND_ROOT = "src.commands"

class CmdTemplate:
    cmd_name = ""

    def run(self, parsed: ParsedArgs, config: Config) -> None:
        raise NotImplementedError()

def load_commands() -> list[CmdTemplate]:
    commands: list[CmdTemplate] = [import_module(f"{COMMAND_ROOT}.{cmd}") for cmd in COMMANDS.keys()]
    commands: list[CmdTemplate] = []
    for module_name in COMMANDS.keys():
        cmd: CmdTemplate = import_module(f"{COMMAND_ROOT}.{module_name}")
        assert isinstance(cmd.cmd_name, str), f"Module '{module_name}' is missing field 'cmd_name'"
        assert cmd.cmd_name == module_name, f"Field 'cmd_name' in module '{module_name}' should be set to '{module_name}'"
        assert callable(cmd.run), f"Module '{module_name}' is missing function 'run'"
        commands.append(cmd)
    return commands
