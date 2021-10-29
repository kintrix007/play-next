import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json, prompt_create_play_json

cmd_name = "reinit"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    title = load_play_json(cwd).title
    prompt_create_play_json(config, title, cwd, True)
    print(f"Successfully reinitialized '{title}'")
