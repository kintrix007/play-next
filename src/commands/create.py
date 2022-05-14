from colorama import Style
from src.play_next_obj import dir_path_from_title, create_episode_dir_symlink, prompt_create_play_json
from src.args import ParsedArgs
from src.status_data import PLANNED, Status
from src.config import Config
from src.link_utilz import link

cmd_name = "create"

def run(parsed: ParsedArgs, config: Config) -> None:
    title = parsed.command.params[0].strip()

    assert not title.startswith("."), "The title must not start with a '.' (dot) character!"

    does_set_status = parsed.get_arg("status")
    status = Status().from_str(does_set_status.params[0]) if does_set_status else PLANNED
    is_starred = parsed.get_arg("star") != None

    series_path = dir_path_from_title(config, title)

    try:
        play_next = prompt_create_play_json(
            config, title, series_path, can_overwrite=False,
            def_status=status,
            def_starred=is_starred,
        )
    except KeyboardInterrupt:
        print("\nAborted.")
        return
    
    create_episode_dir_symlink(series_path, play_next.episode_dir, title)
    
    link(config, series_path)
    
    starred_str = "starred " if is_starred else ""
    print(f"\nSuccessfully added {starred_str}{status} series '{Style.BRIGHT}{play_next.full_title}{Style.RESET_ALL}'")
