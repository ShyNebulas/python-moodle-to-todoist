import typer
from typing import List
from typing_extensions import Annotated

import config

app = typer.Typer()

@app.command()
def path():
    """
    Returns the config path
    """
    config.get_path()

@app.command()
def add(
        words: Annotated[List[str], typer.Argument(help="The word(s) to be added to the blacklist")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add word(s) to the default instead")] = False
    ):
    """
    Add a word(s) to the blacklist
    """
    for word in words:
        config.add(word, "blacklist_default" if default else "blacklist")

@app.command()
def remove(
        words: Annotated[List[str], typer.Argument(help="The word(s) to be removed from the blacklist")] = None,
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False
    ):
    """
    Remove a word(s) from the blacklist
    """
    for word in words:
        config.remove(word, "blacklist_default" if default else "blacklist")

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the blacklist?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clear the default instead")] = False           
    ):
    """
    Clears contents of the blacklist

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        config.remove_all("blacklist_default" if default else "blacklist")

@app.command()
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the blacklist with the default?", help="Force restore without confirmation")] = False):
    """
    Restores blacklist to the default

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        config.restore_to_default("blacklist", "blacklist_default")

@app.callback("blacklist", invoke_without_command=True)
def blacklist(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False):
    """
    Displays contents of the blacklist
    """
    if not config.exists():
        config.create()
    if ctx.invoked_subcommand is None:
        config.contents("blacklist_default" if default else "blacklist")
        
if __name__ == "__main__":
    app()