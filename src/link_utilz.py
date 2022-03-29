import os
from os import path
from src.play_json import PlayNext, load_play_next
from src.status_data import DROPPED, FINISHED, PLANNED, STATUS_STRINGS, WATCHING, Status
from src.config import Config
from colorama import Fore, Style


def _reset_target_link_dirs(config: Config) -> None:
    all_dirs = _get_all_dirs(config)
    for dir in all_dirs:
        if os.path.exists(dir):
            # remove symlink
            link_paths = [p for f in os.listdir(dir) if path.islink(p := path.join(dir, f))]
            for l in link_paths: os.unlink(l)
        else:
            os.makedirs(dir)


def _get_starred_dir(config: Config) -> str:
    return path.join(config.link_root, "starred")

def _get_all_dirs(config: Config) -> list[str]:
    starred_dir = _get_starred_dir(config)
    return [ path.join(config.link_root, x) for x in STATUS_STRINGS ] + [ starred_dir ]

_last_link_root = None
_status_path_map = {}
def _get_link_target_path(config: Config, play_next: PlayNext) -> str:
    global _status_path_map, _last_link_root

    link_root = config.link_root

    if link_root != _last_link_root:
        _status_path_map = { x: path.join(link_root, x) for x in STATUS_STRINGS }
    _last_link_root = link_root
    
    target_dir = _status_path_map[str(play_next.status)]
    return path.join(target_dir, play_next.title)


def link(config: Config, series_path: str) -> None:
    play_next = load_play_next(series_path)
    link_target = _get_link_target_path(config, play_next)

    os.symlink(series_path, link_target)
    
    if play_next.starred:
        starred_dir = _get_starred_dir(config)
        target_path = path.join(starred_dir, play_next.title)
        os.symlink(series_path, target_path)

def relink_all(config: Config) -> None:
    _reset_target_link_dirs(config)

    source_root = config.source_root

    all_series_paths = [ p for f in os.listdir(source_root) if path.isdir(p := path.join(source_root, f)) ]
    for series_path in all_series_paths:
        link(config, series_path)


# def _relink(config: Config, verbose=False) -> None:
#     source_root  = config.source_root
#     link_root  = config.link_root
#     starred_dir  = os.path.join(link_root, "starred")
#     planned_dir  = os.path.join(link_root, "planned")
#     watching_dir = os.path.join(link_root, "watching")
#     dropped_dir  = os.path.join(link_root, "dropped")
#     finished_dir = os.path.join(link_root, "finished")

#     dirs = [ starred_dir, planned_dir, watching_dir, dropped_dir, finished_dir ]
#     _reset_target_link_dirs(dirs, verbose=verbose)
    
#     names = [f for f in os.listdir(source_root) if path.isdir(path.join(source_root, f))]
#     longest = max(map(len, names))# + len(source_root)
#     for series_name in names:
#         series_dir = os.path.join(source_root, series_name)
#         play_next = load_play_next(series_dir)
#         os.chdir(series_dir)

#         def link_to(dir: str, verbose=False, starred=False) -> None:
#             source_dir = path.abspath(series_dir)
#             link_target = path.join(dir, play_next.title)
#             os.symlink(source_dir, link_target)
#             if verbose:
#                 start = f"{Fore.YELLOW}{Style.BRIGHT}" if starred else ""
#                 arrow = "*>" if starred else "->"
#                 print(start + "%-{}s {} %s".format(longest, arrow) % (series_name, path.basename(dir)+"/"), sep="")

#         { str(PLANNED):  lambda: link_to(planned_dir, verbose=verbose)
#         , str(WATCHING): lambda: link_to(watching_dir, verbose=verbose)
#         , str(DROPPED):  lambda: link_to(dropped_dir, verbose=verbose)
#         , str(FINISHED): lambda: link_to(finished_dir, verbose=verbose)
#         } [str(play_next.status)]()

#         if play_next.starred:
#             link_to(starred_dir, verbose=verbose, starred=True)

# def _reset_target_link_dirs(dirs: list[str], verbose=False) -> None:
#     for dir in dirs:
#         if not os.path.exists(dir):
#             os.makedirs(dir)
#         else:
#             link_paths = [p for f in os.listdir(dir) if path.islink(p := path.join(dir, f))]
#             for l in link_paths:
#                 os.unlink(l)
#     if verbose:
#         print("Unlinked previous symlinks")
