from src.command_line_argument import CommandLineArgument, Command, Argument, ParsedArgs
from src.arg_data import COMMANDS, ARGUMENTS, ARG_MAP, DEFAULT_COMMAND
from itertools import chain

def _expand_arg(arg: str) -> list[str]:
    if arg.startswith("--"):  return [ arg ]
    elif arg.startswith("-"): return [f"--{ARG_MAP[letter]}" for letter in arg[1:]]
    else:                     return [ arg ]

def _expand_args(raw_args: list[str]) -> list[str]:
    arg_stop_idx = raw_args.index("--") if "--" in raw_args else len(raw_args)
    parsed_args = [_expand_arg(arg) for arg in raw_args[:arg_stop_idx]]
    unparsed_args = raw_args[arg_stop_idx:]
    return list(chain.from_iterable(parsed_args)) + unparsed_args

#TODO rework argument parsing

def parse_args(in_args: list[str]) -> ParsedArgs:
    expanded = _expand_args(in_args)

    command: Command | None = None
    args:    list[Argument] = []

    params_left = 0
    current_cla: CommandLineArgument | None = None

    def add_arg(current_cla: CommandLineArgument) -> None:
        nonlocal command
        nonlocal args
        assert current_cla != None

        if isinstance(current_cla, Command):
            assert command == None, f"There can be only one command! ('{command.name}', '{current_cla.name}' were given)"
            command = current_cla
        elif isinstance(current_cla, Argument):
            args.append(current_cla)

    arguments_ended = False
    for arg in expanded:
        if arg == "--":
            arguments_ended = True
            continue

        params_left -= 1
        if params_left >= 0: # still need to add params
            assert current_cla != None
            current_cla.params.append(arg)
        if params_left == 0: # params all in
            assert current_cla != None
            add_arg(current_cla)
            current_cla = None
        elif params_left < 0 and not arguments_ended:
            assert current_cla == None
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
    
    assert current_cla == None and params_left <= 0, f"Missing parameters for '{current_cla.name}'"

    return ParsedArgs(command or DEFAULT_COMMAND, args)
