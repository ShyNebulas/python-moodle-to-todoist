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

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if not config.exists():
        config.create()
    if ctx.invoked_subcommand is None:
        print("yes")
        
if __name__ == "__main__":
    app()