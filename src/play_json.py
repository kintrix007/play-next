import json, os
from os import path
from src.utilz import PLAY_JSON
from src.config import Config
from src.status_data import Status
from typing import Union

class PlayJson:
    def __init__(self, play_next: dict) -> None:
        self.title       : str              = play_next["title"]
        self.watched     : int              = play_next["watched"]
        self.ep_count    : Union[int, None] = play_next["ep_count"]
        self.website     : Union[str, None] = play_next["website"]
        self.format      : str              = play_next["format"]
        self.status      : Status           = Status().from_str(play_next["status"])
        self.starred     : bool             = play_next["starred"]
        self.episode_dir : Union[str, None] = play_next["episode_dir"]
    
    def to_dict(self) -> dict:
        return {
            "title":       self.title,
            "watched":     self.watched,
            "ep_count":    self.ep_count,
            "website":     self.website,
            "format":      self.format,
            "status":      self.status.to_str(),
            "starred":     self.starred,
            "episode_dir": self.episode_dir,
        }

def prompt_create_play_json(config: Config, title: str, play_json_dir: str, overwrite=False) -> None:
    play_json_path = path.join(play_json_dir, PLAY_JSON)


    old_play_json = None
    if path.exists(play_json_path):
        assert overwrite, f"File '{play_json_path}' already exists"
        old_play_json = load_play_json(play_json_dir)

    defaults = {
        "ep_count": old_play_json.ep_count if old_play_json else None,
        "website": old_play_json.website if old_play_json else None,
        "format": old_play_json.format if old_play_json else config.default_source_format,
        "episode_dir": old_play_json.episode_dir if old_play_json else config.default_episode_dir,
    }

    default = defaults["ep_count"]
    ep_count = input(f"episode count: ({default}) ") or default
    if ep_count: ep_count = int(ep_count)

    default = defaults["website"]
    website = input(f"website: ({default}) ") or default
    
    default = defaults["format"]
    format = input(f"original file format: ({default}) ") or default

    default = defaults["episode_dir"]
    episode_dir = input(f"episode dir: ({default}) ") or default
    if episode_dir: episode_dir = path.expanduser(path.expandvars(episode_dir))

    play_next = PlayJson({
        "title": title,
        "watched": 0,
        "ep_count": ep_count,
        "website": website,
        "format": format,
        "status": Status().from_str("planned").to_str(),
        "starred": False,
        "episode_dir": episode_dir,
    })
    with open(play_json_path, "w") as f:
        json.dump(play_next.to_dict(), f, indent=2, sort_keys=True)

def load_play_json(play_json_dir: str) -> PlayJson:
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    assert path.exists(play_json_path), f"File '{play_json_path}' does not exist"

    with open(play_json_path, "r") as f:
        play_json_dict = json.load(f)
    return PlayJson(play_json_dict)

def overwrite_play_json(play_json_dir: str, new_play_next: PlayJson) -> None:
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    with open(play_json_path, "w") as f:
        json.dump(new_play_next.to_dict(), f, indent=2, sort_keys=True)
