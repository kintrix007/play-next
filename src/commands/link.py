import os
from typing import Counter
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING
from colorama import Fore, Style

cmd_name = "link"

def run(parsed: ParsedArgs, config: Config) -> None:
    source_root  = config.source_dir
    target_root  = config.target_dir
    starred_dir  = os.path.join(target_root, "starred")
    planned_dir  = os.path.join(target_root, "planned")
    watching_dir = os.path.join(target_root, "watching")
    dropped_dir  = os.path.join(target_root, "dropped")
    finished_dir = os.path.join(target_root, "finished")

    dirs = [ starred_dir, planned_dir, watching_dir, dropped_dir, finished_dir ]
    prepare_dirs(dirs)
    
    names = os.listdir(source_root)
    longest = max(map(len, names)) + len(source_root)
    for series_name in names:
        series_dir = os.path.join(source_root, series_name)

        os.chdir(series_dir)
        def link_to(dir: str, start = "", verbose = True) -> None:
            source_dir = os.path.abspath(play_next.episode_dir)
            link_target = os.path.join(dir, series_name)
            os.symlink(source_dir, link_target)
            if verbose:
                print(start + "%-{}s -> %s".format(longest) % (source_dir, link_target), sep="")

        play_next = load_play_json(series_dir)

        { str(PLANNED):  lambda: link_to(planned_dir)
        , str(WATCHING): lambda: link_to(watching_dir)
        , str(DROPPED):  lambda: link_to(dropped_dir)
        , str(FINISHED): lambda: link_to(finished_dir)
        } [str(play_next.status)]()

        if play_next.starred:
            link_to(starred_dir, start=f"{Fore.YELLOW}{Style.BRIGHT}")


def prepare_dirs(dirs: list[str]) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            links = os.listdir(dir)
            for l in links:
                link_path = os.path.join(dir, l)
                os.unlink(link_path)
