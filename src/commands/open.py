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
    try:
        browser = parsed.get_arg("with").params[0]
    except AttributeError:
        browser = DEFAULT_BROWSER
    print(f"Opening website '{site}'...")
    os.system(f"{browser} {site}")
