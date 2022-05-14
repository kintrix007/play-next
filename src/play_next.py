from __future__ import annotations
from typing import TYPE_CHECKING
import os
from os import path
from src.play_next_obj import dump_play_json, load_play_json
from src.config import Config
from src.status_data import STATUS_STRINGS
from src.utilz import PLAY_JSON, flatten
if TYPE_CHECKING:
    from src.play_next_obj import PlayNextObj


class PlayNext:
    def __init__(self, config: Config, title: str) -> None:
        self.config = config
        self.title = title
    
    @staticmethod
    def create_from_cwd(config: Config) -> PlayNext:
        title = path.basename(os.getcwd())
        return PlayNext(config, title)

    def load(self) -> PlayNextObj:
        return load_play_json(self.config, self.title)
    
    def dump(self, obj: PlayNextObj) -> None:
        dump_play_json(self.config, self.title, obj)
    
    def relink(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.load()
        self.unlink(obj)
        self.link(obj)

    def link(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.load()
        if self.is_linked() == True:
            return
        
        all_targets = self.get_link_targets(self.config, obj)
        for target in all_targets:
            os.symlink(self.get_full_path(), target, target_is_directory=True)

    def unlink(self, obj=None) -> None:
        obj: PlayNextObj = obj or self.load()
        if self.is_linked(obj) == False:
            return
        
        all_targets = self.get_link_targets(self.config, obj)
        for target in all_targets:
            os.unlink(target)

    # * None means partially linked. This means
    # * that some symlinks exist, some don't 
    def is_linked(self, obj=None) -> bool | None:
        obj: PlayNextObj = obj or self.load()

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

    def get_episode_files(self, obj=None) -> list[str]:
        obj: PlayNextObj = obj or self.load()

        cwd = os.getcwd()
        os.chdir(self.get_full_path())

        self_dir_path = path.abspath(".")
        obj_dir_path = path.abspath(path.expanduser(path.expandvars(obj.episode_dir)))
        _master_dir = os.environ.get("PLAY_NEXT_EP_MASTER_DIR")
        master_dir_path = None if _master_dir == None else path.abspath(_master_dir)
        
        os.chdir(cwd)
        
        self_dir_files = [path.join(self_dir_path, f) for f in os.listdir(self_dir_path) if f != PLAY_JSON]
        obj_dir_files = [path.join(obj_dir_path, f) for f in os.listdir(obj_dir_path) if f != PLAY_JSON]
        master_dir_files = [path.join(master_dir_path, obj.title, f) for f in os.listdir(path.join(master_dir_path, obj.title)) if f != PLAY_JSON]

        return [ *self_dir_files, *obj_dir_files, *master_dir_files ]



    def _get_link_targets(self, obj=None) -> list[str]:
        obj: PlayNextObj = obj or self.load()

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
