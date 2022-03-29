import os, json
from os import path
from src.utilz import CONFIG_FILE

class Config:
    def __init__(self, config_dict: dict[str, str]) -> None:
        self._as_dict              = config_dict.copy()
        self.link_root             = config_dict["target_dir"]
        self.source_root           = config_dict["source_dir"]
        self.default_episode_dir   = config_dict["default_episode_dir"]
        self.default_source_format = config_dict["default_source_format"]
        self.default_website       = config_dict["default_website"]
    
    def __str__(self) -> str:
        return str(self._as_dict)

CONFIG_PATH = path.expanduser(f"~/{CONFIG_FILE}")
DEFAULTS: dict[str, str] = {
    "target_dir": path.expanduser("~/Documents/series/"),
    "source_dir": path.expanduser("~/Documents/.series-source/"),
    "default_episode_dir": ".",
    "default_source_format": r"^(?:[^\d]*\d+){0}[^\d]*0*(?P<ep>\d+).*\.(?P<ext>[\w\d]+)$",
    "default_website": "https://www.google.com/search?q={title}",
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

def default_website(config: Config, full_title: str) -> str:
    return config.default_website.format(title=full_title.replace(" ", "%20"))
