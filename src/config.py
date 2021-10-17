import os, json
from os import path

CONFIG_PATH = path.expanduser("~/.play-next.config")
DEFAULTS: dict[str, str] = {
    "target_dir": path.expanduser("~/Documents/anime/"),
    "source_dir": path.expanduser("~/.anime-source/"),
    "default_source_format": r"^(?:[^\d]*\d+){0}[^\d]*0*(?P<episode>\d+).*\.(?P<extension>[\w\d]+)$",
    "target_format": "{title}-{0}.{1}",
}

def prompt_create_config() -> None:
    print("First-time configuration:\n")
    config = DEFAULTS.copy()
    for k, v in config.items():
        res = input(f"{k}: [default={v}] ")
        if res == "": continue
        config[k] = res
        if k in [ "target_dir", "source_dir" ]:
            config[k] = path.expanduser(path.expandvars(config[k]))
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def load_config() -> dict[str, str]:
    if not os.path.exists(CONFIG_PATH):
        prompt_create_config()
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config

