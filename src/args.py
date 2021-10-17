from typing import Union


class CommandLineArgument:
    def __init__(self, name: str, params: list[str]) -> None:
        self.name = name
        self.params = params
    def __str__(self) -> str:
        params = ", ".join(self.params)
        return f"'{self.name}': {params}"

class Command(CommandLineArgument):
    def __str__(self) -> str:
        return "[Command " + super().__str__() + "]"

class Argument(CommandLineArgument):
    def __str__(self) -> str:
        return "[Argument " + super().__str__() + "]"


class ParsedArgs:
    def __init__(self, command: Command, args: list[Argument]) -> None:
        self.command = command
        self.args = args
    def __str__(self) -> str:
        args = "\n".join([str(i) for i in self.args])
        return f"{self.command}\n{args}"


COMMANDS: dict[str, int] = {
    "create": 1,
    "init": 0,
    "open": 0,
    "status": 1,
    "sync": 0,
    "rename": 0
}
ARGUMENTS: dict[str, int] = {
    "with": 1,
    "fave": 0
}
ARG_MAP = {
    "w": "with",
    "f": "fave"
}

args: set[str] = set()


def _expand_args(in_args: list[str]) -> list[str]:
    result = []

    for arg in in_args:
        if arg.startswith("-") and not arg.startswith("--"):
            result += ["--" + ARG_MAP[letter] for letter in arg[1:]]
        else:
            result.append(arg)
            
    return result

def parse_args(in_args: list[str]):
    expanded = _expand_args(in_args)

    command: Union[Command, None] = None
    args:    list[Argument]       = []

    params_left = 0
    current_cla: Union[CommandLineArgument, None] = None

    def add_arg(current_cla: CommandLineArgument) -> None:
        nonlocal command
        nonlocal args
        assert current_cla != None

        if isinstance(current_cla, Command):
            assert command == None, f"There can be only one command! ('{command.name}', '{current_cla.name}' were given)"
            command = current_cla
        elif isinstance(current_cla, Argument):
            args.append(current_cla)

    for arg in expanded:
        params_left -= 1

        if params_left >= 0: # still need to add params
            assert current_cla != None
            current_cla.params.append(arg)
        if params_left == 0: # params all in
            add_arg(current_cla)
                
            current_cla = None
        
        if params_left < 0:
            if arg.startswith("--"):
                arg = arg[2:]
                assert arg in ARGUMENTS, f"'--{arg}' is not a valid argument"
                params_left = ARGUMENTS[arg]
                current_cla = Argument(arg, [])
            else:
                assert arg in COMMANDS, f"'{arg}' is not a valid command"
                params_left = COMMANDS[arg]
                current_cla = Command(arg, [])
            
            if params_left == 0:
                add_arg(current_cla)
                current_cla = None
    
    assert current_cla == None and params_left <= 0, f"Missing parameters for {current_cla.name}"

    return ParsedArgs(command, args)
