import os, re
from os import path
from typing import Callable, Union
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json, get_episodes_path
from src.utilz import PLAY_JSON, TARGET_FORMAT

cmd_name = "rename"

#TODO switch to using `get_episodes_path`

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)

    title = play_next.title
    pattern = re.compile(play_next.format)
    files = sorted(get_episodes_path(play_next, config))
    temp_matches = { path: match for path in files if (match := re.match(pattern, os.path.basename(path))) }
    matches = { path: match for path, match in temp_matches }
    # episodes_dir = os.path.expandvars(os.path.expandvars(play_next.episode_dir or config.default_episode_dir))

    # files_temp = sorted([f for f in os.listdir(episodes_dir) if f != PLAY_JSON])
    # temp_matches = {file: match for file in files_temp if (match := re.match(pattern, file))}
    
    # if len(temp_matches) == 0:
    #     print("No files match the source format")
    #     return

    # matches: dict[str, Union[str, int]] = {}
    # for f, m in temp_matches.items():
    #     groups = m.groups()
    #     groupdict = {k: trydo(v, int, ValueError) for k, v in m.groupdict().items()}
    #     matches[f] = groups, groupdict

    # rename_map = {
    #     src: TARGET_FORMAT.format(*groups, title=title, **groupdict)
    #     for src, (groups, groupdict) in matches.items()
    # }
    
    # indent_left = max(map(len, rename_map.keys()))
    # for k, v in rename_map.items():
    #     # print(("{k:<%d}->{v:>%d}" % (indent_left+2, indent_right+2)).format(k=k, v=v))
    #     print("%-{}s -> %s".format(indent_left+1) % (k, v))

    # res = input("\nIs this correct? (Y/n) ").lower().strip()
    # if res not in [ "", "y", "yes" ]: return

    # for src, dst in rename_map.items():
    #     src_path = os.path.join(episodes_dir, src)
    #     dst_path = os.path.join(episodes_dir, dst)
    #     os.rename(src_path, dst_path)
    # print("Successfully renamed files")


def tryorkeep(on: str, do: Callable, *exceptions: list[Exception]):
    try:
        return do(on)
    except exceptions or Exception:
        return on
