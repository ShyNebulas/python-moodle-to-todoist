import typer
from typing import List
from typing_extensions import Annotated

import config

app = typer.Typer()

@app.command()
def path(default: Annotated[bool, typer.Option("--default", "-d", help="Shows the path of default instead")] = False):
    """
    Returns the config path
    """
    config.get_path("stripped_default" if default else "stripped")

@app.command()
def add(
        words: Annotated[List[str], typer.Argument(help="The word(s) to be added to the stripped list")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add word(s) to the default instead")] = False
    ):
    """
    Add a word(s) to the stripped list
    """
    for word in words:
        config.add(word, "stripped_default" if default else "stripped")

@app.command()
def remove(
        words: Annotated[List[str], typer.Argument(help="The word(s) to be removed from the stripped list")] = None,
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False
    ):
    """
    Remove a word(s) from the stripped list
    """
    for word in words:
        config.remove(word, "stripped_default" if default else "stripped")

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the stripped list?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clear the default instead")] = False           
    ):
    """
    Clears contents of the stripped list

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        config.remove_all("stripped_default" if default else "stripped")

@app.command()
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the stripped list with the default?", help="Force restore without confirmation")] = False):
    """
    Restores stripped list to the default

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        config.restore_to_default("stripped", "stripped_default")

@app.callback()
def stripped(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False):
    """
    Displays contents of the stripped list
    """
    if not config.exists():
        config.create()
    if ctx.invoked_subcommand is None:
        config.contents("stripped_default" if default else "stripped")
        
if __name__ == "__main__":
    app()