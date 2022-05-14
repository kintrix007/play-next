from colorama import Style
import os
from src.play_next import PlayNext
from src.args import ParsedArgs
from src.config import Config
from src.utilz import DEFAULT_BROWSER

cmd_name = "open"

def run(parsed: ParsedArgs, config: Config) -> None:
    play_next = PlayNext.create_from_cwd(config)
    obj = play_next.load()
    website = obj.website

    if website == None:
        print("Website is not specified")
        print(f"Run {Style.BRIGHT}'play-next reinit'{Style.RESET_ALL} to specify it")
        exit(1)
    
    try:
        browser = parsed.get_arg("with").params[0]
    except AttributeError:
        browser = DEFAULT_BROWSER
    
    print(f"Opening website '{website}'...")
    os.system(f"{browser} '{website}'")
