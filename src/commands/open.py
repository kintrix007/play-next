import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json
from src.utilz import DEFAULT_BROWSER

cmd_name = "open"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)
    site = play_next.website
    browser = next((arg.params[0] for arg in parsed.args if arg.name == "with"), DEFAULT_BROWSER)
    print(f"Opening website '{site}'...")
    os.system(f"{browser} {site}")
