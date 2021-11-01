from src.play_json import prompt_create_play_json
from src.args import ParsedArgs
from src.config import Config
from src.utilz import normalize_file_name

cmd_name = "create"

def run(parsed: ParsedArgs, config: Config) -> None:
    title = parsed.command.params[0]

    prompt_create_play_json(config, title, can_overwrite=False)
    print(f"Successfully created '{title}'")
