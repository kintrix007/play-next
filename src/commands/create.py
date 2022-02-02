from src.play_json import dir_path_from_title, make_ep_symlink, prompt_create_play_json
from src.args import ParsedArgs
from src.config import Config

cmd_name = "create"

def run(parsed: ParsedArgs, config: Config) -> None:
    title = parsed.command.params[0]

    source_dir_path = dir_path_from_title(config, title)
    play_next = prompt_create_play_json(config, title, source_dir_path, can_overwrite=False)
    
    make_ep_symlink(source_dir_path, play_next.episode_dir, title)
    
    print(f"Successfully created '{title}'")
