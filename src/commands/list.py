from dis import dis
import os
from os import path
from src.play_json import PlayNext, load_play_json
from src.args import ParsedArgs
from src.config import Config
from colorama import Style, Fore

cmd_name = "list"

def run(parsed: ParsedArgs, config: Config) -> None:
    all_statuses: dict[str, list[str]] = { dir: [] for dir in os.listdir(config.target_dir) }

    for status in all_statuses.keys():
        status_path = path.join(config.target_dir, status)
        sub_dir_names = os.listdir(status_path)
        for dir in sub_dir_names:
            play_next = load_play_json(path.join(status_path, dir))
            all_statuses[status].append(play_next.full_title)
    
    print("\n\n".join([
        Style.BRIGHT + Fore.BLUE
        + "-" * len(s) + "\n"
        + s.capitalize() + ""
        + "\n" + "-" * len(s) + "\n"
        + Style.RESET_ALL
        
        #TODO Make this look good
        + "\n".join([elem for elem in sorted(arr)])
        for s, arr in all_statuses.items()
    ]))
