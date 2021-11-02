import os
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json_nullable, prompt_create_play_json

cmd_name = "reinit"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    filename = os.path.basename(os.path.normpath(cwd))
    play_next = load_play_json_nullable(cwd)
    title = play_next.title if play_next != None else filename
    prompt_create_play_json(config, title, cwd)
    print(f"Successfully reinitialized '{title}'")
    print("DOES NOT PROPERLY RELINK EPISODE DIR SYMLINK")
