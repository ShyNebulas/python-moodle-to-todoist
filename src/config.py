import typer
from rich import print
from pathlib import Path

import _config

import blacklist
import stripped
import projects
import todoist

app = typer.Typer()

app.add_typer(blacklist.app, name="blacklist", help="Manage words to be blacklisted", invoke_without_command=True)
app.add_typer(stripped.app, name="stripped", help="Manage words to be stripped", invoke_without_command=True)
app.add_typer(todoist.app, name="todoist", help="Manage todoist configurations and tags", invoke_without_command=True)

@app.command()
def path():
    """
    Returns the configuration path
    """
    print(_config.get_path())

@app.callback()
def config(ctx: typer.Context):
    if not _config.exists():
        result: tuple[Path, Path] = _config.create()
        for value in result: print(f"Created {value}")

if __name__ == "__main__":
    app()