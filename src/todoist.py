import typer
from rich import print
from typing_extensions import Annotated

import _config

import tags
import projects

app = typer.Typer()

app.add_typer(tags.app, name="tags", help="Manage tag list", invoke_without_command=True)
app.add_typer(projects.app, name="projects", help="Manage todoist projects", invoke_without_command=True)

@app.command()
def key(key: Annotated[str, typer.Argument(help="The Todoist key to be set")]):
    """
    Setting Todoist key
    """
    try:
        added: bool = _config.add_value("todoist_key", key)
        print(f"'{key}' {'was added to the' if added else 'already exists in'} 'todoist_key'")
    except KeyError as error:
        print(error)
    
@app.callback()
def todoist(ctx: typer.Context):
    """
    Displays the set Todoist key
    """
    if ctx.invoked_subcommand is None:
        try:
            print(_config.get_value("todoist_key"))
        except KeyError as error:
            print(error)

if __name__ == "__main__":
    app()