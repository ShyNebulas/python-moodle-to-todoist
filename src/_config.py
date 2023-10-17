import typer
from pathlib import Path
import json

default = {
    "folder": None,
    "blacklist": [],
    "blacklist_default": ["attendance", "booking", "discussion", "folder", "forum", "handbook", "reading", "selection", "session", "slides", "solution", "submission", "support", "weekly", "zoom", "overview"],
    "stripped": [],
    "stripped_default": ["file", "link", "page", "reading", "video", "web", "toggle"],
    "tags": {},
    "tags_default": {},
    "projects": {},
    "projects_default": {},
    "todoist_key": None
}

APP_NAME = "python-moodle-to-todoist"

DIRECTORY_PATH = Path(typer.get_app_dir(APP_NAME))
CONFIG_PATH = DIRECTORY_PATH / ".config.json"

def get_path() -> Path:
    return CONFIG_PATH

def exists() -> bool:
    return CONFIG_PATH.is_file()
    
def create() -> tuple[Path, Path]:
    directory: Path = None
    config: Path = None
    if not DIRECTORY_PATH.is_dir():
        DIRECTORY_PATH.mkdir(mode=0o777, parents=False, exist_ok=True)
        directory = DIRECTORY_PATH
    if not CONFIG_PATH.exists():
        CONFIG_PATH.touch(mode=0o666, exist_ok=True)
        config = CONFIG_PATH
    with CONFIG_PATH.open(mode="w", encoding="utf-8") as file:
        json.dump(default, file, indent=4)
    return (directory, config)

def get_value(key: str) -> str | list[str]:
    with CONFIG_PATH.open(mode="r+", encoding="utf-8") as file:
        json_contents: json = json.load(file)
        if key not in json_contents: raise KeyError(f"'{key}' does not exist in '{CONFIG_PATH}'")
        return json_contents[key]

def add_value(key: str, value: tuple[str, str] | list[str] | str) -> bool:
    with CONFIG_PATH.open(mode="r+", encoding="utf-8") as file:
        json_contents: json = json.load(file)
        if key not in json_contents: raise KeyError(f"'{key}' does not exist in '{CONFIG_PATH}'")
        match json_contents[key]:
            case dict():
                dict_key: str = value[0]
                dict_value: str = value[1]
                if dict_key in json_contents[key]:
                    if dict_value == json_contents[key][dict_key]: return False
                json_contents[key][dict_key] = dict_value
            case list():
                if value in json_contents[key]: return False
                json_contents[key].append(value)
            case _:
                if value == json_contents[key]: return False
                json_contents[key] = str(value)
        file.seek(0)
        json.dump(json_contents, file, indent=4)
        file.truncate()
        return True

def remove_value(key: str, value: tuple[str,] | list[str] | str) -> bool:
    with CONFIG_PATH.open(mode="r+", encoding="utf-8") as file:
        json_contents: json = json.load(file)
        if key not in json_contents: raise Exception(f"'{key}' does not exist in '{CONFIG_PATH}'")
        match json_contents[key]:
            case dict():
                if value[0] not in json_contents[key]: return False
                del json_contents[key][value[0]]
            case list():
                if value not in json_contents[key]: return False
                json_contents[key].remove(value)
            case str():
                if value != json_contents[key]: return False
                json_contents[key] = None
        file.seek(0)
        json.dump(json_contents, file, indent=4)
        file.truncate()
        return True
    

        