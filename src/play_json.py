import os, json
from os import path
from src.utilz import PLAY_JSON, compose, normalize_file_name, to_title_format
from src.config import Config
from src.status_data import PLANNED, Status

class PlayNext:
    def __init__(self, play_json: dict) -> None:
        self.title       : str        = play_json["title"]
        # self.full_title  : str | None = None if "full_title" not in play_json else play_json["full_title"] #! Don't allow for `None` anymore
        self.full_title  : str        = play_json["full_title"]
        self.watched     : int        = play_json["watched"]
        self.ep_count    : int | None = play_json["ep_count"]
        self.website     : str | None = play_json["website"]
        self.format      : str        = play_json["format"]
        self.status      : Status     = Status().from_str(play_json["status"])
        self.starred     : bool       = play_json["starred"]
        self.episode_dir : str | None = play_json["episode_dir"]
    
    def to_dict(self) -> dict:
        return {
            "title":       self.title,
            "full_title":  self.full_title,
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
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    # assert not (not can_overwrite and path.exists(play_json_path)), f"'{play_json_dir}' already exists!"
    assert not path.exists(play_json_path) or can_overwrite, f"'{play_json_dir}' already exists!"

    old_play_next = load_play_json_nullable(play_json_dir)

    play_json = {
        "title":       old_play_next.title       if old_play_next else title,
        "full_title":  old_play_next.full_title  if old_play_next else to_title_format(title),
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

    prompt("full_title")
    prompt("ep_count", int, ValueError, nullable=True)
    prompt("website")
    prompt("format")
    prompt("episode_dir")

    play_next = PlayNext(play_json)
    
    if not path.exists(play_json_dir):
        os.mkdir(play_json_dir)

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

def load_play_json_nullable(play_json_dir: str) -> PlayNext | None:
    try:
        return load_play_json(play_json_dir)
    except AssertionError:
        return None
    

def overwrite_play_json(play_json_dir: str, new_play_next: PlayNext) -> None:
    play_json_path = path.join(play_json_dir, PLAY_JSON)
    with open(play_json_path, "w") as f:
        json.dump(new_play_next.to_dict(), f, indent=2, sort_keys=True)


def get_episodes_path(play_next: PlayNext, config: Config):
    expand = compose(path.expanduser, path.expandvars)
    ep_dir = expand(play_next.episode_dir or config.default_episode_dir)
    ep_paths  = [path.join(ep_dir, f) for f in os.listdir(ep_dir) if f != PLAY_JSON] if path.exists(ep_dir) else []
    cwd = os.getcwd()
    cwd_paths = [path.join(cwd, f) for f in os.listdir(cwd) if f != PLAY_JSON]
    return ep_paths + cwd_paths
