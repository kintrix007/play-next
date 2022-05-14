import os
from src.args import ParsedArgs
from src.config import Config
from src.play_next_obj import get_episode_files, load_play_next, overwrite_play_json
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING
from src.utilz import DEFAULT_PLAYER, TARGET_FORMAT
from colorama import Style

cmd_name = "play"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_next(cwd)

    next_ep = play_next.watched + 1
    next_ep_name_start = TARGET_FORMAT.format(title=play_next.title, ep=next_ep, ext="")

    files = get_episode_files(cwd)

    try:
        next_ep_path = next(f for f in files if os.path.basename(f).startswith(next_ep_name_start))
    except StopIteration:
        print(f"Next episode ({next_ep}) does not exist or is not named properly")
        print(f"Execute {Style.BRIGHT}'play-next rename'{Style.RESET_ALL} to fix the naming of the files")
        return

    try:
        player = parsed.get_arg("with").params[0]
    except AttributeError:
        player = DEFAULT_PLAYER

    print(f"{player} '{next_ep_path}'")
    exit_code = os.system(f"{player} '{next_ep_path}'")
    assert exit_code == 0, f"'{player}' stopped with a non-zero exit code ({exit_code})"

    play_next.watched = next_ep

    was_status_updated = False
    if play_next.ep_count != None and play_next.watched >= play_next.ep_count:
        play_next.status = FINISHED
        was_status_updated = True
    elif play_next.status == PLANNED or play_next.status == DROPPED:
        play_next.status = WATCHING
        was_status_updated = True
    
    overwrite_play_json(cwd, play_next)

    print("\n")
    print(f"Finished playing episode {next_ep}")
    if was_status_updated: print(f"Status has been updated to '{play_next.status}'")
