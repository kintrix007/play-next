#!/usr/bin/env python3

# Simple script to quickly change something in all the json files

import os
from src.config import default_website, load_config
from src.play_json import get_episode_files, load_play_json_nullable, overwrite_play_json, dir_path_from_title
from src.utilz import to_title_format

config = load_config()
all_titles = get_episode_files(config)

for title in all_titles:
    dir_path = dir_path_from_title(config, title)
    play_next = load_play_json_nullable(dir_path)
    if play_next == None: continue
    if play_next.website == None:
        play_next.website = default_website(config, play_next.full_title)
    # overwrite_play_json(dir_path, play_next)
    print(f"Converted '{play_next.title}' as '{play_next.website}'")
