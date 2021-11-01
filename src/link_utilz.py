import os
from src.play_json import load_play_json
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING
from src.utilz import PLAY_JSON
from src.config import Config
from colorama import Fore, Style


def relink(config: Config, verbose=False) -> None:
    source_root  = config.source_dir
    target_root  = config.target_dir
    starred_dir  = os.path.join(target_root, "starred")
    planned_dir  = os.path.join(target_root, "planned")
    watching_dir = os.path.join(target_root, "watching")
    dropped_dir  = os.path.join(target_root, "dropped")
    finished_dir = os.path.join(target_root, "finished")

    dirs = [ starred_dir, planned_dir, watching_dir, dropped_dir, finished_dir ]
    prepare_dirs(dirs, verbose=verbose)
    
    names = os.listdir(source_root)
    longest = max(map(len, names)) + len(source_root)
    for series_name in names:
        series_dir = os.path.join(source_root, series_name)
        play_next = load_play_json(series_dir)
        os.chdir(series_dir)

        def link_to(dir: str, start = "", verbose=False) -> None:
            source_dir = os.path.abspath(play_next.episode_dir)
            link_target = os.path.join(dir, play_next.title)
            os.symlink(source_dir, link_target)
            if verbose:
                print(start + "%-{}s -> %s".format(longest) % (source_dir, link_target), sep="")


        { str(PLANNED):  lambda: link_to(planned_dir, verbose=verbose)
        , str(WATCHING): lambda: link_to(watching_dir, verbose=verbose)
        , str(DROPPED):  lambda: link_to(dropped_dir, verbose=verbose)
        , str(FINISHED): lambda: link_to(finished_dir, verbose=verbose)
        } [str(play_next.status)]()

        if play_next.starred:
            link_to(starred_dir, verbose=verbose, start=f"{Fore.YELLOW}{Style.BRIGHT}")

def prepare_dirs(dirs: list[str], verbose=False) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            links = os.listdir(dir)
            for l in links:
                link_path = os.path.join(dir, l)
                os.unlink(link_path)
    if verbose:
        print("Unlinked previous symlinks")