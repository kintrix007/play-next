import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_next, overwrite_play_json

cmd_name = "seek"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_next(cwd)
    seek_ep = parsed.command.params[0]

    if seek_ep[0] in [ "+", "-" ]:
        play_next.watched += int(seek_ep)
    else:
        play_next.watched = int(seek_ep) - 1
    
    play_next.watched = max(0, play_next.watched)
    if play_next.ep_count: play_next.watched = min(play_next.ep_count, play_next.watched)
    overwrite_play_json(cwd, play_next)
    print(f"Next episode will be ep '{play_next.watched+1}'")
