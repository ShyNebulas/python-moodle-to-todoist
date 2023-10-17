import typer
from rich import print
from typing_extensions import Annotated

import _config

which_key = lambda default: "projects_default" if default else "projects"

app = typer.Typer()

@app.command()
def add(
        project: Annotated[tuple[str, str], typer.Argument(help="The project to be added to the projects list")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add project to the default project list instead")] = False
    ):
    """
    Add a project to the project list
    """
    try:
        added: bool = _config.add_value(which_key(default), project)
        print(f"'{project}' {'was added to the' if added else 'already exists in the'} '{which_key(default)}'")
    except KeyError as error:
        print(error)

@app.command()
def remove(
        key: Annotated[str, typer.Argument(help="The key to be removed from the project list")] = None,
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default project list instead")] = False
    ):
    """
    Remove a key, and it's pair, from the project list
    """
    try:
        removed: bool = _config.remove_value(which_key(default), ((key),))
        print(f"'{key}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}'")
    except KeyError as error:
        print(error)

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the project list?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clear the default project list instead")] = False           
    ):
    """
    Clears contents of the project list

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            keys: dict = _config.get_value(which_key(default))
            for key in keys:
                print(key)
                removed: bool = _config.remove_value(which_key(default), ((key),))
                print(f"'{key}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}'")
            print(f"The contents of the '{which_key(default)}' was cleared")
        except KeyError as error:
            print(error)

@app.command()
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the project list with the default project list?", help="Force restore without confirmation")] = False):
    """
    Restores project list to the default

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            project_dict: dict = _config.get_value("projects")
            for key in project_dict:
                removed: bool = _config.remove_value("projects", ((key),))
                print(f"'{key}' {'was removed from the' if removed else 'does not exists in the'} 'projects'")
            print(f"The contents of 'projects' was cleared")
            default_dict: dict = _config.get_value("projects_default")
            for key in default_dict:
                added: bool = _config.add_value("projects", (key, default_dict[key]))
                print(f"'{key}' {'was added to the' if added else 'already exists in the'} 'projects'")
            print(f"The contents of 'projects' have been restored")
        except KeyError as error:
            print(error)

@app.callback()
def projects(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False):
    """
    Displays contents of the project list
    """
    if ctx.invoked_subcommand is None:
        try:
            print(_config.get_value(which_key(default)))
        except KeyError as error:
            print(error)
        
if __name__ == "__main__":
    app()