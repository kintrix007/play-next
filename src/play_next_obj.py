from __future__ import annotations
import os
import json
from os import path
from src.utilz import EPISODE_SYMLINK_NAME, PLAY_JSON, is_same_path, normalize_file_name, normalized_abs_path, to_title_format
from src.config import Config, default_website
from src.status_data import PLANNED, Status

class PlayNextObj:
    def __init__(self, play_json: dict) -> None:
        self.title       : str        = play_json["title"]
        self.full_title  : str        = play_json["full_title"]
        self.status      : Status     = Status.from_str(play_json["status"])
        self.watched     : int        = play_json["watched"]
        self.ep_count    : int | None = play_json.get("ep_count")
        self.website     : str        = play_json["website"]
        self.format      : str        = play_json["format"]
        self.episode_dir : str        = play_json["episode_dir"]
        self.starred     : bool       = play_json.get("starred") or False
        self.seasonal    : bool       = play_json.get("seasonal") or False
        self.local       : bool       = play_json.get("local") or False
        assert self.episode_dir != None
    
    def to_dict(self) -> dict:
        return {
            "title":       self.title,
            "full_title":  self.full_title,
            "status":      str(self.status),
            "watched":     self.watched,
            "ep_count":    self.ep_count,
            "website":     self.website,
            "format":      self.format,
            "episode_dir": self.episode_dir,
            "starred":     self.starred,
            "seasonal":    self.seasonal,
            "local":       self.local,
        }


def load_play_json(config: Config, title: str) -> PlayNextObj:
    return _load_play_json_from_path(path.join(config.source_root, title))

def load_play_json_nullable(config: Config, title: str) -> PlayNextObj | None:
    try:
        return load_play_json(config, title)
    except FileNotFoundError:
        return None

def dump_play_json(config: Config, title: str, new_obj: PlayNextObj) -> None:
    play_json_path = path.join(config.source_root, title, PLAY_JSON)

    with open(play_json_path, "w") as f:
        json.dump(new_obj.to_dict(), f, indent=2, sort_keys=True)
        

def get_series_titles(config: Config) -> list[str]:
    all_paths = [p for f in os.listdir(config.source_root) if not f.startswith(".") and path.isdir(p := path.join(config.source_root, f))]
    all_titles = [_load_play_json_from_path(p).title for p in all_paths]
    for i in range(len(all_paths)):
        parent_dir, dirname = path.split(all_paths[i])
        title = all_titles[i]
        if dirname != title:
            raise FileNotFoundError(f"'{path.join(parent_dir, dirname)}' is named incorrectly.\nIt should be '{path.join(parent_dir, title)}'")

    return all_titles


def prompt_create_play_json(config: Config, title: str, to_dir: str, can_overwrite: bool, def_starred: bool = None, def_status: Status = None):
    # TODO Rewrite this

    raise NotImplementedError()
    
    play_json_dir = to_dir
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    # assert not (not can_overwrite and path.exists(play_json_path)), f"'{play_json_dir}' already exists!"
    assert not path.exists(play_json_path) or can_overwrite, f"'{play_json_dir}' already exists!"

    old_play_next = __load_play_json_nullable(play_json_dir)

    full_title = old_play_next.full_title if old_play_next else to_title_format(title)
    play_json = {
        "title":       old_play_next.title       if old_play_next else title,
        "full_title":  full_title,
        "watched":     old_play_next.watched     if old_play_next else 0,
        "status":      str(old_play_next.status) if old_play_next else str(def_status) if def_status else str(PLANNED),
        "starred":     old_play_next.starred     if old_play_next else def_starred or False,
        "ep_count":    old_play_next.ep_count    if old_play_next else None,
        "website":     old_play_next.website     if old_play_next else default_website(config, full_title),
        "format":      old_play_next.format      if old_play_next else config.default_source_format,
        "episode_dir": old_play_next.episode_dir if old_play_next else config.default_episode_dir,
    }

    def prompt(key: str, do=lambda x:x, *exceptions: list[Exception], nullable=False) -> None:
        prev = play_json[key]
        try:
            res = input(f"{key}: ({prev}) ") or prev
            play_json[key] = None if nullable and res == None else do(res)
        except exceptions or Exception:
            print("Incorrect format")
            prompt(key, do)

    prompt("full_title")
    prompt("ep_count", int, ValueError, nullable=True)
    prompt("website")
    # prompt("format")
    prompt("episode_dir")

    play_next = PlayNextObj(play_json)
    
    if not path.exists(play_json_dir):
        os.mkdir(play_json_dir)

    with open(play_json_path, "w") as f:
        as_text = json.dumps(play_next.to_dict(), indent=2, sort_keys=True)
        f.write(as_text)
    
    return play_next

def create_episode_dir_symlink(source_dir_path: str, relative_ep_dir_path: str, title: str, verbose=True) -> None:
    # TODO Rewrite this
    
    prev_dir = os.getcwd()
    os.chdir(source_dir_path)

    ep_dir_path = normalized_abs_path(relative_ep_dir_path)
    if not (path.isdir(ep_dir_path) and path.samefile(ep_dir_path, source_dir_path)):
        ep_dir_name = path.basename(path.abspath(ep_dir_path))
        if ep_dir_name == title:
            os.symlink(ep_dir_path, path.join(source_dir_path, EPISODE_SYMLINK_NAME))
        else:
            sub_ep_dir_path = path.join(ep_dir_path, title)
            if path.isdir(ep_dir_path):
                if not path.isdir(sub_ep_dir_path):
                    os.mkdir(sub_ep_dir_path)
                    if verbose: print(f"Created directory '{sub_ep_dir_path}'")
            elif verbose:
                print(f"Could not create directory '{sub_ep_dir_path}', because its parent directory does not exist")

            os.symlink(sub_ep_dir_path, os.path.join(source_dir_path, EPISODE_SYMLINK_NAME))
    
    os.chdir(prev_dir)


def _load_play_json_from_path(dir_path: str) -> PlayNextObj:
    play_json_path = path.join(dir_path, PLAY_JSON)
    if not path.exists(play_json_path):
        raise FileNotFoundError(f"File '{play_json_path}' does not exist")

    with open(play_json_path, "r") as f:
        play_json_dict = json.load(f)

    return PlayNextObj(play_json_dict)
