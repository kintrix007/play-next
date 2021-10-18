import re


PLAY_JSON = ".play.json"
CONFIG_FILE = ".play-next.config"

def normalize_file_name(title: str) -> str:
    prev_result = ""
    result = title.lower()
    while prev_result != result:
        prev_result = result
        result = re.sub(r"[^a-zA-Z0-9\-]", "-", prev_result)
    
    prev_result = ""
    result = result.strip("-")
    while prev_result != result:
        prev_result = result
        result = re.sub(r"-+", "-", prev_result)
    
    return result

