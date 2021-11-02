import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json_nullable, prompt_create_play_json
from utilz import EPISODE_SYMLINK_NAME, is_same_path, normalized_abs_path

cmd_name = "reinit"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    prev_play_next = load_play_json_nullable(cwd)
    filename = os.path.basename(os.path.normpath(cwd))
    title = prev_play_next.title if prev_play_next != None else filename
    
    play_next = prompt_create_play_json(config, title, cwd)

    ep_symlink_path = os.path.join(cwd, EPISODE_SYMLINK_NAME)
    if os.path.islink(ep_symlink_path):
        os.unlink(ep_symlink_path)
    
    if not is_same_path(play_next.episode_dir, cwd):
        ep_dir = normalized_abs_path(play_next.episode_dir)
        os.symlink(ep_dir, ep_symlink_path)
    
    print(f"Successfully reinitialized '{title}'")
