import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json, overwrite_play_json
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING
from src.utilz import DEFAULT_PLAYER, PLAY_JSON, TARGET_FORMAT
from colorama import Style

cmd_name = "play"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)
    files = sorted([f for f in os.listdir(play_next.episode_dir) if f != PLAY_JSON])
    prev_ep = play_next.watched
    next_ep = prev_ep + 1
    ep_name_start = TARGET_FORMAT.format(title=play_next.title, ep=next_ep, ext="")

    try:
        next_ep_name = next(f for f in files if f.startswith(ep_name_start))
    except StopIteration:
        print("Next episode does not exist or is not named properly")
        print(f"run {Style.BRIGHT}'play-next rename'{Style.RESET_ALL} to fix the naming of the files")
        return
    
    next_ep_path = os.path.join(play_next.episode_dir, next_ep_name)

    try:
        player = parsed.get_arg("with").params[0]
    except AttributeError:
        player = DEFAULT_PLAYER

    exit_code = os.system(f"{player} '{next_ep_path}'")
    assert exit_code == 0, f"'{player}' stopped with a non-zero exit code ({exit_code})"

    play_next.watched = next_ep

    was_status_updated = False
    if play_next.watched >= play_next.ep_count:
        play_next.status = FINISHED
        was_status_updated = True
    elif play_next.status == PLANNED or play_next.status == DROPPED:
        play_next.status = WATCHING
        was_status_updated = True
    
    overwrite_play_json(cwd, play_next)

    print("\n")
    print(f"Finished playing episode {next_ep}")
    if was_status_updated: print(f"Status has been updated to '{play_next.status}'")
