from src.args import ParsedArgs
from src.config import Config
from src.link_utilz import relink_all  

cmd_name = "link"

def run(parsed: ParsedArgs, config: Config) -> None:
    verbose = parsed.get_arg("verbose") != None
    relink_all(config)
