from src.command_line_argument import Command

DEFAULT_COMMAND = Command("play", [])

COMMANDS: dict[str, int] = {
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

ARGUMENTS: dict[str, int] = {
    "verbose": 0,
    "with": 1,
}

ARG_MAP = {
    "a": "all",
    "v": "verbose",
    "w": "with",
}
