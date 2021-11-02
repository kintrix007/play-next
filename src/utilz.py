import re
from os import path
from typing import Any, Callable
from functools import reduce


PLAY_JSON = ".play.json"
CONFIG_FILE = ".play-next.config"
EPISODE_SYMLINK_NAME = "episodes"
DEFAULT_BROWSER = "firefox"
DEFAULT_PLAYER = "vlc --fullscreen"
TARGET_FORMAT = "{title}-{ep:02d}.{ext}"


def normalize_file_name(title: str) -> str:
    prev_result = ""
    result = title.lower()
    while prev_result != result:
        prev_result = result
        result = re.sub(r"[^a-zA-Z0-9\-]", "-", prev_result)
    
    prev_result = ""
    result = result.strip("-")
    while prev_result != result:
        prev_result = result
        result = re.sub(r"-+", "-", prev_result)
    
    return result

def normalized_abs_path(p: str) -> str:
    norm = compose(path.abspath, path.normcase, path.normpath, path.expanduser, path.expandvars)
    return norm(p)

def is_same_path(path1: str, path2: str) -> bool:
    norm1 = normalized_abs_path(path1)
    norm2 = normalized_abs_path(path2)
    return norm1 == norm2

def compose(*functions: list[Callable[[Any], Any]]) -> Callable[[Any], Any]: 
    def comp(f: Callable, g: Callable):
        return lambda x: f(g(x))
    return reduce(comp, functions)
