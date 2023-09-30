import typer
from typing import List
from typing_extensions import Annotated

import config

app = typer.Typer()

@app.command()
def add(words: Annotated[List[str], typer.Argument(help="The word(s) to be added to the blacklist")]):
    """
    Add a word(s) to the blacklist
    """
    for word in words:
        config.add(word, "blacklist")

@app.command()
def remove(words: Annotated[List[str], typer.Argument(help="The word(s) to be removed from the blacklist")]):
    """
    Remove a word(s) from the blacklist
    """
    for word in words:
        config.remove(word, "blacklist")

@app.command()
def remove_all(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the blacklist?", help="Force deletion without confirmation")] = False):
    """
    Clears contents of the blacklist

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        config.remove_all("blacklist")

@app.callback(invoke_without_command=True)
def blacklist_callback(ctx: typer.Context):
    """
    Displays contents of the blacklist
    """
    if not config.exists():
        config.create()
    if ctx.invoked_subcommand is None:
        config.contents("blacklist")
        
if __name__ == "__main__":
    app()