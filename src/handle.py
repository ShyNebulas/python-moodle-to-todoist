import typer
from pathlib import Path

import _config

def key_not_set(key: str):
    print(f"{key} has not been set")
    confirm: bool = typer.confirm(f"Set {key} value")
    if confirm:
        value: str = typer.prompt("Value")
        added: bool = _config.add_value(key, value)
        print(f"'{value}' {'was added to' if added else 'already exists in'} {key}")


        
