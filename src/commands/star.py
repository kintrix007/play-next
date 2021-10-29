import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json, overwrite_play_json

cmd_name = "star"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    play_next.starred = True
    overwrite_play_json(cwd, play_next)
    print(f"Successfully starred this series")