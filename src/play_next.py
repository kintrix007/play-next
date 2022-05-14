import json
import os
from os import path
from src.play_next_obj import PlayNextObj
from src.config import Config
from src.utilz import PLAY_JSON
from src.status_data import STATUS_STRINGS


class PlayNext:
    def __init__(self, config: Config, title: str) -> None:
        self.config = config
        self.title = title
    
    def read(self) -> PlayNextObj:
        return load_play_json(self.config, self.title)
    
    def write(self, obj: PlayNextObj) -> None:
        dump_play_json(self.config, self.title, obj)
    
    def relink(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.read()
        self.unlink(obj)
        self.link(obj)

    def link(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.read()
        if self.is_linked() == True:
            return
        
        all_targets = self.get_link_targets(self.config, obj)
        for target in all_targets:
            os.symlink(self.get_full_path(), target, target_is_directory=True)

    def unlink(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.read()
        if self.is_linked(obj) == False:
            return
        
        all_targets = self.get_link_targets(self.config, obj)
        for target in all_targets:
            os.unlink(target)

    # * None means partially linked. This means
    # * that some symlinks exist, some don't 
    def is_linked(self, obj=None) -> bool | None:
        obj: PlayNextObj = obj or self.read()

        all_targets = self._get_link_targets(self.config, obj)
        full_path = self.get_full_path()
        is_linked: bool | None = None
        is_partially_linked = False

        for target in all_targets:
            if path.samefile(full_path, target):
                if is_linked == False:
                    is_partially_linked = True
                is_linked = True
            else:
                if is_linked == True:
                    is_partially_linked = True
                is_linked = False
        
        if is_partially_linked: return None

        return is_linked

    def get_full_path(self) -> str:
        return path.join(self.config.source_root, self.title)


    def _get_link_targets(self, obj=None) -> list[str]:
        obj: PlayNextObj = obj or self.read()

        if obj.local: return []

        link_root = self.config.link_root
        all_targets = []
        
        for status in STATUS_STRINGS:
            if obj.status == status:
                all_targets.append(path.join(link_root, status))
                break
        
        if obj.starred:
            all_targets.append(path.join(link_root, "starred"))
        if obj.seasonal:
            all_targets.append(path.join(link_root, "seasonal"))
        


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


def _load_play_json_from_path(dir_path: str) -> PlayNextObj:
    play_json_path = path.join(dir_path, PLAY_JSON)
    if not path.exists(play_json_path):
        raise FileNotFoundError(f"File '{play_json_path}' does not exist")

    with open(play_json_path, "r") as f:
        play_json_dict = json.load(f)
    
    return PlayNextObj(play_json_dict) 
