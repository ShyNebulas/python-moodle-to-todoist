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
    """Returns path of JSON files

    Returns:
        Path: Path of JSON file
    """
    return CONFIG_PATH

def exists() -> bool:
    """Checks that JSON exists

    Returns:
        bool: True on JSON existance; false otherwise
    """
    return CONFIG_PATH.is_file()
    
def create() -> tuple[Path, Path]:
    """Creates the JSON file and/or it's parent directory if neither already exist

    Returns:
        tuple[Path, Path]: Returns the paths of the JSON file and/or parent directory if created, else returns None in it's place
    """
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
    """Returns value(s) of given key

    Args:
        key (str): The corresponding JSON key

    Raises:
        FileExistsError: JSON file does not exist
        KeyError: JSON file does not contain given key

    Returns:
        str | list: The value(s) from the JSON corresponding with the given key
    """
    with CONFIG_PATH.open(mode="r+", encoding="utf-8") as file:
        json_contents: json = json.load(file)
        if key not in json_contents: raise KeyError(f"'{key}' does not exist in '{CONFIG_PATH}'")
        return json_contents[key]

def add_value(key: str, value: tuple[str, str] | list[str] | str) -> bool:
    """Adds a value to the corresponding key in a JSON file

    Args:
        key (str): The corresponding JSON key
        value (str | list): The value(s) to be added to the given JSON key

    Raises:
        FileExistsError: JSON file does not exist
        KeyError: JSON file does not contain given key

    Returns:
        bool: False when given key already contain given value; true when given value has been added to given key
    """
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
    """Removes a value to the corresponding key in a JSON file

    Args:
        key (str): The corresponding JSON key
        value (str | list): The value(s) to be removed from the given JSON key

    Raises:
        FileExistsError: JSON file does not exist
        KeyError: JSON file does not contain given key

    Returns:
        bool: False when given key does not contain given value; true when given value has been removed from the given key
    """
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
    

        