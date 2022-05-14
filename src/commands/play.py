import os
from src.play_next import PlayNext
from src.args import ParsedArgs
from src.config import Config
from src.status_data import DROPPED, FINISHED, PLANNED, WATCHING
from src.utilz import DEFAULT_PLAYER, TARGET_FORMAT
from colorama import Style

cmd_name = "play"

def run(parsed: ParsedArgs, config: Config) -> None:
    play_next = PlayNext.create_from_cwd(config)
    obj = play_next.load()

    next_ep = obj.watched + 1
    next_ep_name_start = TARGET_FORMAT.format(title=obj.title, ep=next_ep, ext="")

    files = play_next.get_episode_files()

    try:
        next_ep_path = next(f for f in files if os.path.basename(f).startswith(next_ep_name_start))
    except StopIteration as e:
        print(f"Next episode ({next_ep}) does not exist or is not named properly")
        print(f"Execute {Style.BRIGHT}'play-next rename'{Style.RESET_ALL} to fix the naming of the files")
        raise Exception() from e

    try:
        player = parsed.get_arg("with").params[0]
    except AttributeError:
        player = DEFAULT_PLAYER

    print(f"{player} '{next_ep_path}'")
    exit_code = os.system(f"{player} '{next_ep_path}'")
    if exit_code != 0:
        raise OSError(f"'{player}' stopped with a non-zero exit code ({exit_code})")

    obj.watched = next_ep

    was_status_updated = False
    if obj.ep_count != None and obj.watched >= obj.ep_count:
        obj.status = FINISHED
        was_status_updated = True
    elif obj.status == PLANNED or obj.status == DROPPED:
        obj.status = WATCHING
        was_status_updated = True
    
    play_next.dump(obj)

    print("\n")
    print(f"Finished playing episode {next_ep}")
    if was_status_updated: print(f"Status has been updated to '{obj.status}'")
