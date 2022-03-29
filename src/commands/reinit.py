import os
from os import path
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json_nullable, create_episode_dir_symlink, prompt_create_play_json
from src.utilz import EPISODE_SYMLINK_NAME, is_same_path

cmd_name = "reinit"

def run(parsed: ParsedArgs, config: Config) -> None:
    source_dir_path = os.getcwd()
    
    prev_play_next = load_play_json_nullable(source_dir_path)
    source_dir_name = path.basename(path.normpath(source_dir_path))

    title = prev_play_next.title if prev_play_next != None else source_dir_name
    
    play_next = prompt_create_play_json(config, title, source_dir_path, can_overwrite=True)

    episode_dir_symlink_path = path.join(source_dir_path, EPISODE_SYMLINK_NAME)
    if path.islink(episode_dir_symlink_path):
        os.unlink(episode_dir_symlink_path)
    create_episode_dir_symlink(source_dir_path, play_next.episode_dir, title)
    
    print(f"Successfully reinitialized '{title}'")
