import os, json
from os import path
from src.utilz import CONFIG_FILE

class Config:
    def __init__(self, config_dict: dict[str, str]) -> None:
        self._as_dict              = config_dict.copy()
        self.target_dir            = config_dict["target_dir"]
        self.source_dir            = config_dict["source_dir"]
        self.default_episode_dir   = config_dict["default_episode_dir"]
        self.default_source_format = config_dict["default_source_format"]
        self.target_format         = config_dict["target_format"]
    
    def __str__(self) -> str:
        return str(self._as_dict)

CONFIG_PATH = path.expanduser(f"~/{CONFIG_FILE}")
DEFAULTS: dict[str, str] = {
    "target_dir": path.expanduser("~/Documents/series/"),
    "source_dir": path.expanduser("~/Documents/.series-source/"),
    "default_episode_dir": ".",
    "default_source_format": r"^(?:[^\d]*\d+){0}[^\d]*0*(?P<ep>\d+).*\.(?P<ext>[\w\d]+)$",
    "target_format": "{title}-{ep:02d}.{ext}",
}

def prompt_create_config() -> None:
    print("First time configuration needed. By pressing enter you accept the default.\n")
    config = DEFAULTS.copy()
    for k, v in config.items():
        res = input(f"{k}: ({v}) ")
        if res == "": continue
        config[k] = res
        if k in [ "target_dir", "source_dir" ]:
            config[k] = path.expanduser(path.expandvars(config[k]))
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def load_config() -> Config:
    if not os.path.exists(CONFIG_PATH):
        prompt_create_config()
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return Config(config)
