import os
from os import path
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json

cmd_name = "info"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    title = play_next.title
    starred = play_next.starred
    status = str(play_next.status).capitalize()
    watched = play_next.watched
    ep_count = play_next.ep_count
    episode_dir = play_next.episode_dir

    print(f"{title} - {status}{'[*]' if starred else ''}")
    if ep_count == None:
        print(f"Watched {watched} eps")
    else:
        print(f"Watched {watched} of {ep_count}")
    
    if not parsed.get_arg("full"): return
    if episode_dir:
        print()
        print(f"Episode directory: '{episode_dir}'")
