from src.command_line_argument import CommandLineArgument, Command, Argument, ParsedArgs
from src.arg_data import COMMANDS, ARGUMENTS, ARG_MAP, DEFAULT_COMMAND

def _expand_args(in_args: list[str]) -> list[str]:
    result = []

    arguments_ended = False
    for arg in in_args:
        if arg == "--":
            arguments_ended = True
            result.append(arg)
        elif arg.startswith("-") and not arg.startswith("--") and not arguments_ended:
            # assert all([letter in ARG_MAP for letter in arg[1:]]) # * Will get a KeyError without it, so it is unneded
            result += ["--" + ARG_MAP[letter] for letter in arg[1:]]
        else:
            result.append(arg)
            
    return result

def parse_args(in_args: list[str]):
    expanded = _expand_args(in_args)

    command: Command = DEFAULT_COMMAND
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

    return ParsedArgs(command, args)
