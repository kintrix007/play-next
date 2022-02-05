import os, re
from os import path
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json
from src.utilz import EPISODE_SYMLINK_NAME, PLAY_JSON, TARGET_FORMAT

cmd_name = "rename"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    inter_files = os.listdir(cwd)
    exter_files_path = path.join(cwd, EPISODE_SYMLINK_NAME)
    exter_files = os.listdir(exter_files_path) if path.exists(exter_files_path) else []
    files = [f for f in inter_files + exter_files if f != PLAY_JSON]

    title = play_next.title
    pattern = re.compile(play_next.format)

    matches = {
        filepath: (match.groups(), { k: try_parse_int(v) for k, v in match.groupdict().items() })
        for filepath in files
        if (match := re.match(pattern, path.basename(filepath))) != None
    }

    if len(matches) == 0:
        return print("No files match the source format")

    rename_map = {
        src: dst for src, (groups, groupdict) in matches.items()
        if src != (dst := path.join(path.dirname(src), TARGET_FORMAT.format(*groups, title=title, **groupdict)))
    }

    if len(rename_map) == 0:
        return print("All files are already named properly")

    longest_source = max(map(lambda x: len(path.basename(x)), rename_map.keys()))
    for src, dst in rename_map.items():
        src_base = path.basename(src)
        dst_base = path.basename(dst)
        print("%-{}s -> %s".format(longest_source) % (src_base, dst_base))
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
