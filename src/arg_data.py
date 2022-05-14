from src.command_line_argument import Command

DEFAULT_COMMAND = Command("play", [])

COMMAND_PARAM_COUNTS = {
    "play": 0,
    "open": 0,
    "create": 1,
    "reinit": 0,
    "status": 1,
    "info": 0,
    "list": 0,
    "link": 0,
    "rename": 0,
    "star": 0,
    "seek": 1,
}

ALWAYS_POSSIBLE_ARGUMENTS = [ "help" ]

COMMAND_POSSIBLE_ARGUMENTS = {
    "play":   [ "quiet", "with" ],
    "open":   [ "quiet", "with" ],
    "create": [ "status", "star", "yes" ],
    "reinit": [ "status", "star", "unstar", "yes" ],
    "status": [ "verbose" ],
    "info":   [ "verbose" ],
    "list":   [ "pretty" ],
    "link":   [ "verbose" ],
    "rename": [ "yes" ],
    "star":   [ "verbose", "delete" ],
    "seek":   [ "verbose" ],
}

ARGUMENT_PARAM_COUNTS = {
    "star": 0,      # --star
    "delete": 0,    # --delete
    "status": 1,    # --status
    "verbose": 0,   # --verbose
    "with": 1,      # --with
    "quiet": 0,     # --quiet
    "yes": 0,       # --yes
}

SHORT_ARG_MAP = {
    "s": "star",
    "u": "unstar",
    "t": "status",
    "v": "verbose",
    "w": "with",
    "q": "quiet",
    "y": "yes",
}
