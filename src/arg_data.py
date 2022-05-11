from src.command_line_argument import Command

DEFAULT_COMMAND = Command("play", [])

COMMAND_PARAM_COUNTS = {
    "create": 1,
    "info": 0,
    "link": 0,
    "list": 0,
    "open": 0,
    "play": 0,
    "reinit": 0,
    "rename": 0,
    "seek": 1,
    "star": 0,
    "status": 1,
    "unstar": 0,
}

ALWAYS_POSSIBLE_ARGUMENTS = [ "help" ]

COMMAND_POSSIBLE_ARGUMENTS = {
    "create": [ "star", "status", "verbose" ],
    "info": [ "verbose" ],
    "link": [ "verbose" ],
    "list": [ "pretty" ],
    "open": [ "with" ],
    "play": [ "with" ],
    "reinit": [],
    "rename": [],
    "seek": [],
    "star": [],
    "status": [],
    "unstar": [],
}

ARGUMENT_PARAM_COUNTS = {
    "star": 0,
    "status": 1,
    "verbose": 0,
    "with": 1,
}

SHORT_ARG_MAP = {
    "S": "star",
    "s": "status",
    "v": "verbose",
    "w": "with",
}
