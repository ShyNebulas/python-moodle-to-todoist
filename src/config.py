import typer
from pathlib import Path
import json

from themes import console

APP_NAME = "python-moodle-to-todoist"

default = {
    "blacklist": ["attendance", "booking", "discussion", "folder", "forum", "handbook", "reading", "selection", "session", "slides", "solution", "submission", "support", "weekly", "zoom"]
}

directory_path = Path(typer.get_app_dir(APP_NAME))
config_path = directory_path / "config.json"

def exists():
    return config_path.is_file()
    
def create():
    if not directory_path.is_dir():
        directory_path.mkdir(mode=0o777, parents=False, exist_ok=True)
        console.print(f"Created {directory_path}")
    config_path.touch(mode=0o666, exist_ok=True)
    console.print(f"Created {config_path}")
    with config_path.open(mode="w", encoding="utf-8") as file:
        json.dump(default, file, indent=4)

def contents(key: str):
    with config_path.open(mode="r+", encoding="utf-8") as file:
        json_contents = json.load(file)
        console.print(json_contents[key])

def add(word: str, key: str):
    with config_path.open(mode="r+", encoding="utf-8") as file:
        updated_json = json.load(file)
        if word not in updated_json[key]:
            updated_json[key].append(word)
            file.seek(0)
            json.dump(updated_json, file, indent=4)
            console.print(f"'{word}' added to {key}")
        else:
            console.print(f"'{word}' already exists within the {key}")

def remove(word: str, key: str):
     print(config_path)
     with config_path.open(mode="r+", encoding="utf-8") as file:
        updated_json = json.load(file)
        if word in updated_json[key]:
            updated_json[key].remove(word)
            file.seek(0)
            json.dump(updated_json, file, indent=4)
            file.truncate()
            console.print(f"'{word}' removed from {key}")
        else:
            console.print(f"'{word}' doesn't exist within the {key}")
    
def remove_all(key: str):
    with config_path.open(mode="r+", encoding="utf-8") as file:
        updated_json = json.load(file)
        updated_json[key].clear()
        file.seek(0)
        json.dump(updated_json, file, indent=4)
        file.truncate()
        console.print(f"Cleared contents of {key}")


        