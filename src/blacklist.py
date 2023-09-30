import typer
from typing_extensions import Annotated

import config

app = typer.Typer()

@app.command()
def add(word: Annotated[str, typer.Argument(help="The word to be added to the blacklist")]):
    """
    Add a word to the blacklist
    """
    config.add(word, "blacklist")

@app.command()
def remove(word: Annotated[str, typer.Argument(help="The word to be removed from the blacklist")]):
    """
    Remove a word from the blacklist
    """
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