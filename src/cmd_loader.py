from src.config import Config
from src.arg_data import COMMAND_PARAM_COUNTS
from src.command_line_argument import ParsedArgs
from importlib import import_module

COMMAND_ROOT = "src.commands"

class CmdTemplate:
    cmd_name = ""

    def run(self, parsed: ParsedArgs, config: Config) -> None:
        raise NotImplementedError()

def load_commands() -> list[CmdTemplate]:
    commands: list[CmdTemplate] = []
    for module_name in COMMAND_PARAM_COUNTS.keys():
        if module_name not in [ "info", "open", "play", "rename" ]: continue
        cmd: CmdTemplate = import_module(f"{COMMAND_ROOT}.{module_name}")

        if not isinstance(cmd.cmd_name, str):
            raise AttributeError(f"Module '{module_name}' is missing field 'cmd_name'")
        if not cmd.cmd_name == module_name:
            raise AttributeError(f"Field 'cmd_name' in module '{module_name}' should be set to '{module_name}'")
        if not callable(cmd.run):
            raise AttributeError(f"Module '{module_name}' is missing function 'run'")
        
        commands.append(cmd)
    return commands
