import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json
from colorama import Fore, Style
BRIGHT = Style.BRIGHT
NORMAL = Style.NORMAL

cmd_name = "info"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    title = play_next.title
    star_str = f"{Fore.YELLOW}[*]{Fore.RESET}" if play_next.starred else ""
    status = str(play_next.status).capitalize()
    watched = play_next.watched
    ep_count = play_next.ep_count
    episode_dir = play_next.episode_dir
    website = play_next.website

    print(f"{BRIGHT}{title}{NORMAL} - {BRIGHT}{status} {star_str}")
    if ep_count == None:
        print(f"Watched {watched} eps")
    else:
        print(f"Watched {watched} of {ep_count} eps")
    
    if not parsed.get_arg("full"): return
    if episode_dir:
        print()
        print(f"Episode directory: '{episode_dir}'")
    if website:
        print(f"Website: '{website}'")

