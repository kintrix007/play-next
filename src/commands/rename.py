import os, re
from typing import Callable, Union
from src.args import ParsedArgs
from src.config import Config
from src.play_json import load_play_json

cmd_name = "rename"

def run(parsed: ParsedArgs, config: Config) -> None:
    cwd = os.getcwd()
    play_next = load_play_json(cwd)
    title = play_next.title
    source_format = play_next.format
    target_format = config.target_format
    pattern = re.compile(source_format)

    files_temp = [file for file in os.listdir(cwd) if file != ".play.json"]
    temp_matches = {file: match for file in files_temp if (match := re.match(pattern, file))}
    
    matches: dict[str, Union[str, int]] = {}
    for f, m in temp_matches.items():
        groups = m.groups()
        groupdict = {k: trydo(v, int, ValueError) for k, v in m.groupdict().items()}
        matches[f] = groups, groupdict

    rename_map = {
        src: target_format.format(*match[1], title=title, **match[1])
        for src, match in matches.items()
    }
    
    indent_left = max(map(len, matches.keys()))
    indent_right = max(map(len, rename_map.values()))
    for k, v in rename_map.items():
        print(("{k:<%d}->{v:>%d}" % (indent_left+2, indent_right+2)).format(k=k, v=v))

    res = input("\nIs this correct? (y/N) ").lower().strip()
    if res not in [ "y", "yes" ]: return

    for src, dst in rename_map.items():
        src_path = os.path.join(cwd, src)
        dst_path = os.path.join(cwd, dst)
        os.rename(src_path, dst_path)
    print("Successfully renamed files")


def trydo(on: str, do: Callable, *exceptions: list[Exception]):
    try:
        return do(on)
    except exceptions or Exception:
        return on
