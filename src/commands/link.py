from src.args import ParsedArgs
from src.config import Config
from src.link_utilz import relink

cmd_name = "link"

def run(parsed: ParsedArgs, config: Config) -> None:
    relink(config, verbose=True)
