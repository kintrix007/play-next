import os
from os import path
from src.play_json import PlayNext, load_play_next
from src.args import ParsedArgs
from src.config import Config
from colorama import Style, Fore, Back
from src.utilz import clamp_length
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING


cmd_name = "list"

def run(parsed: ParsedArgs, config: Config) -> None:
    all_titles = map(lambda x: load_play_next(path.join(config.source_root, x)), os.listdir(config.source_root))
    
    statuses: dict[str, list[PlayNext]] = {}
    for play_next in all_titles:
        if play_next.status.to_str() not in statuses: statuses[play_next.status.to_str()] = []
        statuses[play_next.status.to_str()].append(play_next)
    
    table = [
        ("finished", sorted(statuses[FINISHED.to_str()], key=lambda x: x.full_title)),
        ("watching", sorted(statuses[WATCHING.to_str()], key=lambda x: x.full_title)),
        ("planned",  sorted(statuses[PLANNED.to_str()],  key=lambda x: x.full_title)),
        ("dropped",  sorted(statuses[DROPPED.to_str()],  key=lambda x: x.full_title)),
    ]

    for k, v in table:
        print("\n\n" + format_header(k), end="\n\n")
        for play_next in v:
            print(format_title(play_next))

def format_header(header: str, indent: int = 1) -> str:
        return (Style.BRIGHT + Fore.BLUE
            + " " * indent + ".-" + "-" * len(header)   + "-." + " " * indent + "\n" 
            + " " * indent + "| " + header.capitalize() + " |" + " " * indent + "\n"
            + " " * indent + "'-" + "-" * len(header)   + "-'" + " " * indent + "\n"
        + Style.RESET_ALL)

def format_title(play_next: PlayNext) -> str:
    starred = (
        Style.BRIGHT + Fore.YELLOW + "[*]" + Style.RESET_ALL
        if play_next.starred else
        Style.DIM + "[ ]" + Style.RESET_ALL
    )
    ep_progress_max_len = 9
    width, _ = os.get_terminal_size()
    width -= 10 + ep_progress_max_len

    ep_progress = f"({play_next.watched}/" + ("??" if play_next.ep_count == None else f"{play_next.ep_count}") + ")"
    ep_progress = "%{}s".format(ep_progress_max_len) % ep_progress
    result = starred + "  " + "%-{}s".format(width) % clamp_length(play_next.full_title, width) + " |"
    if play_next.status in [ WATCHING, DROPPED ]: result += " " + ep_progress
    return result
