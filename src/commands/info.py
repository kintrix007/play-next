from colorama import Fore, Style
from src.play_next import PlayNext
from src.args import ParsedArgs
from src.config import Config
BRIGHT = Style.BRIGHT
NORMAL = Style.NORMAL

cmd_name = "info"
prefix = " "

def run(parsed: ParsedArgs, config: Config) -> None:
    play_next = PlayNext.create_from_cwd(config)
    obj = play_next.load()

    title = obj.full_title
    star_str = f"{Fore.YELLOW}[*]{Fore.RESET}" if obj.starred else ""
    status = str(obj.status).capitalize()
    watched = obj.watched
    ep_count = obj.ep_count
    episode_dir = obj.episode_dir
    website = obj.website

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

