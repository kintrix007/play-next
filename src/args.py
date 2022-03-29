from src.command_line_argument import Command, Argument, ParsedArgs
from src.arg_data import COMMAND_PARAM_COUNTS, ARGUMENT_PARAM_COUNTS, SHORT_ARG_MAP, DEFAULT_COMMAND
from itertools import chain

def _expand_arg(arg: str) -> list[str]:
    if arg.startswith("--"):
        return [ arg ]
    elif arg.startswith("-"):
        expanded_args = []
        for letter in arg[1:]:
            assert letter in SHORT_ARG_MAP, f"'-{letter}' is not a valid argument\n Did you mean '-- {arg}'?"
            expanded_args.append(f"--{SHORT_ARG_MAP[letter]}") 
        return expanded_args
    else:
        return [ arg ]

def _expand_all_args(raw_args: list[str]) -> list[str]:
    arg_stop_idx = raw_args.index("--") if "--" in raw_args else len(raw_args)
    parsed_args = [_expand_arg(arg) for arg in raw_args[:arg_stop_idx]]
    unparsed_args = raw_args[arg_stop_idx:]
    return list(chain.from_iterable(parsed_args)) + unparsed_args

def parse_args(in_args: list[str]) -> ParsedArgs:
    expanded_args = _expand_all_args(in_args)

    command: Command | None = None
    args: list[Argument] = []
    args_ended = False

    command_params_left = -1
    i = 0
    while i < len(expanded_args):
        elem = expanded_args[i]
        if elem == "--":
            args_ended = True
            i += 1; continue
        
        if not args_ended and elem.startswith("--"):
            elem = elem[2:]
            assert elem in ARGUMENT_PARAM_COUNTS, f"'--{elem}' is not a valid argument"
            argument = Argument(elem, [])
            i += 1
            for _ in range(ARGUMENT_PARAM_COUNTS[argument.name]):
                assert i < len(expanded_args), f"Missing parameters for argument '--{argument.name}'"
                elem = expanded_args[i]
                argument.params.append(elem)
                i += 1
            args.append(argument)
            continue
        else:
            if command == None:
                assert elem in COMMAND_PARAM_COUNTS, f"'{elem}' is not a valid sub-command"
                command = Command(elem, [])
                command_params_left = COMMAND_PARAM_COUNTS[command.name]
            else:
                assert command_params_left != -1, "Uhhhhh... This should never happen..."
                assert command_params_left > 0, f"Did not expect any more arguments: '{elem}'"
                command.params.append(elem)
                command_params_left -= 1

        i += 1
    
    if command_params_left == -1:
        assert command == None, f"Ran into a problem defaulting to sub-command '{DEFAULT_COMMAND.name}'"
    else:
        assert command_params_left == 0, f"Missing parameters for sub-command '{command.name}'"

    return ParsedArgs(command or DEFAULT_COMMAND, args)

