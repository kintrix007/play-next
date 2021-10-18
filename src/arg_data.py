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
    def __init__(self, command: Union[Command, None], args: list[Argument]) -> None:
        self.command = command or DEFAULT_COMMAND
        self.args = args
    def __str__(self) -> str:
        args = "\n".join([str(i) for i in self.args])
        return f"{self.command}\n{args}"


DEFAULT_COMMAND = Command("play", [])

COMMANDS: dict[str, int] = {
    "play": 0,
    "create": 1,
    "open": 0,
    "status": 1,
    "sync": 0,
    "rename": 0,
    "star": 0,
    "info": 0,
}
ARGUMENTS: dict[str, int] = {
    "with": 1,
}
ARG_MAP = {
    "w": "with",
}
