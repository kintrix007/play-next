import os
from src.args import ParsedArgs
from src.config import Config
from src.play_next_obj import load_play_next
from colorama import Fore, Style
BRIGHT = Style.BRIGHT
NORMAL = Style.NORMAL

cmd_name = "info"
prefix = " "

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_next(cwd)

    title = play_next.full_title
    star_str = f"{Fore.YELLOW}[*]{Fore.RESET}" if play_next.starred else ""
    status = str(play_next.status).capitalize()
    watched = play_next.watched
    ep_count = play_next.ep_count
    episode_dir = play_next.episode_dir
    website = play_next.website

    print(f"{prefix}{BRIGHT}{title}{NORMAL} [{status}] {BRIGHT}{star_str}")
    if ep_count == None:
        print(f"{prefix}Watched {watched} eps")
    else:
        print(f"{prefix}Watched {watched}/{ep_count} eps")
    
    if not parsed.get_arg("verbose"): return
    if episode_dir:
        print()
        print(f"{prefix}Episode directory: '{episode_dir}'")
    if website:
        print(f"{prefix}Website: '{website}'")

