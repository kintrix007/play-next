import os, json
from os import path
from src.utilz import PLAY_JSON, compose, is_same_path, normalize_file_name
from src.config import Config
from src.status_data import PLANNED, Status
from typing import Union

class PlayNext:
    def __init__(self, play_json: dict) -> None:
        self.title       : str              = play_json["title"]
        self.watched     : int              = play_json["watched"]
        self.ep_count    : Union[int, None] = play_json["ep_count"]
        self.website     : Union[str, None] = play_json["website"]
        self.format      : str              = play_json["format"]
        self.status      : Status           = Status().from_str(play_json["status"])
        self.starred     : bool             = play_json["starred"]
        self.episode_dir : Union[str, None] = play_json["episode_dir"]
    
    def to_dict(self) -> dict:
        return {
            "title":       self.title,
            "watched":     self.watched,
            "ep_count":    self.ep_count,
            "website":     self.website,
            "format":      self.format,
            "status":      str(self.status),
            "starred":     self.starred,
            "episode_dir": self.episode_dir,
        }

def dir_path_from_title(config: Config, title: str) -> str:
    norm_title = normalize_file_name(title)
    return path.join(config.source_dir, norm_title)

def prompt_create_play_json(config: Config, title: str, to_dir: str, can_overwrite=True):
    play_json_dir = to_dir
    if not path.exists(play_json_dir):
        os.mkdir(play_json_dir)
    
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    assert not (not can_overwrite and path.exists(play_json_path)), f"'{play_json_dir}' already exists!"

    old_play_next = load_play_json_nullable(play_json_dir)

    play_json = {
        "title":       old_play_next.title       if old_play_next else title,
        "watched":     old_play_next.watched     if old_play_next else 0,
        "status":      str(old_play_next.status) if old_play_next else str(PLANNED),
        "starred":     old_play_next.starred     if old_play_next else False,
        "ep_count":    old_play_next.ep_count    if old_play_next else None,
        "website":     old_play_next.website     if old_play_next else None,
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

    prompt("ep_count", int, ValueError, nullable=True)
    prompt("website")
    prompt("format")
    prompt("episode_dir", compose(path.expanduser, path.expandvars), None, nullable=True)

    play_next = PlayNext(play_json)
    
    with open(play_json_path, "w") as f:
        as_text = json.dumps(play_next.to_dict(), indent=2, sort_keys=True)
        f.write(as_text)
    
    return play_next


def load_play_json(play_json_dir: str) -> PlayNext:
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    assert path.exists(play_json_path), f"File '{play_json_path}' does not exist"

    with open(play_json_path, "r") as f:
        play_json_dict = json.load(f)
    return PlayNext(play_json_dict)

def load_play_json_nullable(play_json_dir: str) -> Union[PlayNext, None]:
    try:
        return load_play_json(play_json_dir)
    except AssertionError:
        return None
    

def overwrite_play_json(play_json_dir: str, new_play_next: PlayNext) -> None:
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    with open(play_json_path, "w") as f:
        json.dump(new_play_next.to_dict(), f, indent=2, sort_keys=True)
