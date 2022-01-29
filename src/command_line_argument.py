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
        
    def get_arg(self, name: str) -> Argument | None:
        return next((arg for arg in self.args if arg.name == name), None)
    
    def __str__(self) -> str:
        args = "\n".join([str(i) for i in self.args])
        return f"{self.command}\n{args}"
