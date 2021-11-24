import os, re
from os import path
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json, get_episodes_path
from src.utilz import TARGET_FORMAT

cmd_name = "rename"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    title = play_next.title
    pattern = re.compile(play_next.format)
    files = sorted(get_episodes_path(play_next, config))
    
    matches = {
        filepath: (match.groups(), { k: try_parse_int(v) for k, v in match.groupdict().items() })
        for filepath in files
        if (match := re.match(pattern, path.basename(filepath))) != None
    }

    if len(matches) == 0:
        return print("No files match the source format")

    rename_map = {
        src: path.join(path.dirname(src), TARGET_FORMAT.format(*groups, title=title, **groupdict))
        for src, (groups, groupdict) in matches.items()
    }

    longest_source = max(map(len, rename_map.keys()))
    for src, dst in rename_map.items():
        print("'%-{}s' -> '%s'".format(longest_source) % (path.basename(src), path.basename(dst)))
        # print("'%-{}s' -> '%s'".format(longest_source) % (src, dst))
    
    res = input("\nIs this correct (Y/n) ").lower().strip()
    if res in [ "", "y", "yes" ]:
        for src, dst in rename_map.items():
            os.rename(src, dst)
        print("Successfully renamed files")
    else:
        print("Aborted")


def try_parse_int(on: str):
    try:
        return int(on)
    except ValueError:
        return on
