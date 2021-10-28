import os
from src.args import ParsedArgs
from src.config import Config
from src.status_data import Status
from src.play_json import load_play_json, overwrite_play_json

cmd_name = "status"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    new_status_str = parsed.command.params[0]
    new_status = Status().from_str(new_status_str)
    play_next.status = new_status
    overwrite_play_json(cwd, play_next)
    print(f"Successfully set status to '{new_status}'")
