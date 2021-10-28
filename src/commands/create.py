import os
from os import path
from src.play_json import prompt_create_play_json
from src.args import ParsedArgs
from src.config import Config
from src.utilz import normalize_file_name

cmd_name = "create"

def run(parsed: ParsedArgs, config: Config) -> None:
    root_dir = config.source_dir
    title = parsed.command.params[0]
    normalized_title = normalize_file_name(title)
    dir_path = path.join(root_dir, normalized_title)
    if not path.exists(dir_path):
        os.mkdir(dir_path)

    # Will throw if the play json already exists
    prompt_create_play_json(config, title, dir_path)
