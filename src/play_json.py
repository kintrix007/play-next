import json
from os import path
from src.config import Config
import src.utilz as utilz

class PlayJson:
    def __init__(self, play_next: dict) -> None:
        self.title       = play_next["title"]
        self.watched     = play_next["watched"]
        self.ep_count    = play_next["ep_count"]
        self.website     = play_next["website"]
        self.format      = play_next["format"]
        self.status      = play_next["status"]
        self.starred     = play_next["starred"]
        self.episode_dir = play_next["episode_dir"]
    
    def to_dict(self) -> dict:
        return {
            "title":       self.title,
            "watched":     self.watched,
            "ep_count":    self.ep_count,
            "website":     self.website,
            "format":      self.format,
            "status":      self.status,
            "starred":     self.starred,
            "episode_dir": self.episode_dir,
        }

def prompt_create_play_json(config: Config, title: str, play_json_path: str) -> None:
    assert not path.exists(play_json_path), f"File '{play_json_path}' already exists"

    ep_count = input("episode count: (unknown) ") or None
    if ep_count: ep_count = int(ep_count)

    website = input("website: (unknown) ") or None
    
    default = config.default_source_format
    format = input(f"original file format: ({default}) ") or default

    episode_dir = input("episode dir: (config default) ") or None
    if episode_dir: episode_dir = path.expanduser(path.expandvars(episode_dir))

    play_next = PlayJson({
        "title": title,
        "watched": 0,
        "ep_count": ep_count,
        "website": website,
        "format": format,
        "status": str(utilz.Planned()),
        "starred": False,
        "episode_dir": None,
    })

    with open(play_json_path, "w") as f:
        json.dump(play_next.to_dict(), f, indent=2, sort_keys=True)
    print(f"Successfully created '{play_json_path}'")

def load_play_json(play_json_path: str) -> PlayJson:
    assert path.exists(play_json_path), f"File '{play_json_path}' does not exist"

    with open(play_json_path, "r") as f:
        play_json_dict = json.load(f)
    return PlayJson(play_json_dict)
