import os
from src.play_json import dir_path_from_title, load_play_json, prompt_create_play_json
from src.args import ParsedArgs
from src.config import Config
from src.utilz import is_same_path, normalized_abs_path

cmd_name = "create"

def run(parsed: ParsedArgs, config: Config) -> None:
    title = parsed.command.params[0]

    dir_path = dir_path_from_title(config, title)
    play_next = prompt_create_play_json(config, title, dir_path, can_overwrite=False)
    
    if not is_same_path(play_next.episode_dir, dir_path):
        ep_dir = normalized_abs_path(play_next.episode_dir)
        os.symlink(ep_dir, os.path.join(dir_path, "episodes"))
    
    print(f"Successfully created '{title}'")
