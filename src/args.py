from src.command_line_argument import Command, Argument, ParsedArgs
from src.arg_data import COMMAND_PARAM_COUNTS, ARGUMENT_PARAM_COUNTS, COMMAND_POSSIBLE_ARGUMENTS, SHORT_ARG_MAP, DEFAULT_COMMAND
from src.utilz import flatten
import re


class ArgumentParseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def _expand_arg(arg: str) -> list[str]:
    # if arg.startswith("-") and not arg.startswith("--"):
    if re.match(r"^-[^\-]", arg):
        expanded_args = []
        
        for letter in arg[1:]:
            if letter not in SHORT_ARG_MAP: break

            expanded_args.append(f"--{SHORT_ARG_MAP[letter]}") 
        else:
            return expanded_args
    
    return [ arg ]

def _expand_all_args(raw_args: list[str]) -> list[str]:
    arg_stop_idx = raw_args.index("--") if "--" in raw_args else len(raw_args)

    parsed_args = [_expand_arg(arg) for arg in raw_args[:arg_stop_idx]]
    unparsed_args = raw_args[arg_stop_idx:]
    
    return flatten(parsed_args) + unparsed_args


# TODO rewrite without asserts
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
            if elem not in ARGUMENT_PARAM_COUNTS:
                raise ArgumentParseException(f"'--{elem}' is not a valid argument")
            
            argument = Argument(elem, [])
            
            for _ in range(ARGUMENT_PARAM_COUNTS[argument.name]):
                i += 1

                if i >= len(expanded_args):
                    raise ArgumentParseException(f"Missing parameters for argument '--{argument.name}'")
                
                elem = expanded_args[i]
                argument.params.append(elem)
            
            args.append(argument)
        else:
            if command == None:
                if elem not in COMMAND_PARAM_COUNTS:
                    raise ArgumentParseException(f"'{elem}' is not a valid command")
                
                command = Command(elem, [])
                command_params_left = COMMAND_PARAM_COUNTS[command.name]
            else:
                if command_params_left <= 0:
                    raise ArgumentParseException(f"Did not expect any more arguments: '{elem}'")
                
                command.params.append(elem)
                command_params_left -= 1

        i += 1
    
        if command_params_left == -1 and command != None:
            raise ArgumentParseException(f"Ran into a problem defaulting to command '{DEFAULT_COMMAND.name}'...")
    
    if command_params_left > 0:
        raise ArgumentParseException(f"Missing parameters for command '{command.name}'")

    command = command or DEFAULT_COMMAND

    for arg in args:
        if arg.name not in COMMAND_POSSIBLE_ARGUMENTS[command.name]:
            raise ArgumentParseException(f"'--{arg.name}' is not a valid argument for command '{command.name}'")

    return ParsedArgs(command, args)

