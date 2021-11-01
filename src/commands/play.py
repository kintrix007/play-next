import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json

cmd_name = "play"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)
    raise NotImplementedError()