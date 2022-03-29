import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_next
from src.utilz import DEFAULT_BROWSER
from colorama import Style

cmd_name = "open"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_next(cwd)
    site = play_next.website

    if site == None:
        print("Website is not specified")
        print(f"Run {Style.BRIGHT}'play-next reinit'{Style.RESET_ALL} to specify it")
        exit(1)
    
    try:
        browser = parsed.get_arg("with").params[0]
    except AttributeError:
        browser = DEFAULT_BROWSER
    
    print(f"Opening website '{site}'...")
    os.system(f"{browser} '{site}'")
