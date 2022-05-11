import os
from os import path
from src.play_json import PlayNext, get_series_dirs, load_play_next
from src.status_data import STATUS_STRINGS
from src.config import Config


def _reset_target_link_dirs(config: Config) -> None:
    all_dirs = _get_all_target_dirs(config)
    for dir in all_dirs:
        if os.path.exists(dir):
            # remove symlink
            link_paths = [p for f in os.listdir(dir) if path.islink(p := path.join(dir, f))]
            for l in link_paths: os.unlink(l)
        else:
            os.makedirs(dir)


def _get_starred_target_dir(config: Config) -> str:
    return path.join(config.link_root, "starred")

def _get_all_target_dirs(config: Config) -> list[str]:
    starred_dir = _get_starred_target_dir(config)
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
    # ! Quickly hacked it here, not sure if it's enough to make it work
    filename = path.basename(series_path)
    if filename.startswith("."): return

    play_next = load_play_next(series_path)
    link_target = _get_link_target_path(config, play_next)

    os.symlink(series_path, link_target)
    
    if play_next.starred:
        starred_dir = _get_starred_target_dir(config)
        target_path = path.join(starred_dir, play_next.title)
        os.symlink(series_path, target_path)

def relink_all(config: Config) -> None:
    _reset_target_link_dirs(config)

    all_series_paths = get_series_dirs(config, True)
    for series_path in all_series_paths:
        link(config, series_path)
