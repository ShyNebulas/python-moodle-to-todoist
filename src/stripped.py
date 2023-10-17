import typer
from rich import print
from typing_extensions import Annotated

import _config

which_key = lambda default: "stripped_default" if default else "stripped"

app = typer.Typer()

@app.command()
def add(
        words: Annotated[list[str], typer.Argument(help="The word(s) to be added to the stripped list")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add word(s) to the default stripped list instead")] = False
    ):
    """
    Add a word(s) to the stripped list
    """
    for word in words:
        try:
            added = _config.add_value(which_key(default), word)
            print(f"'{word}' {'was added to the' if added else 'already exists in the'} '{which_key(default)}' list")
        except KeyError as error:
            print(error)
                
@app.command()
def remove(
        words: Annotated[list[str], typer.Argument(help="The word(s) to be removed from the stripped list")],
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of the default stripped list instead")] = False
    ):
    """
    Remove a word(s) from the stripped list
    """
    for word in words:
        try:
            removed = _config.remove_value(which_key(default), word)
            print(f"'{word}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}' list")
        except KeyError as error:
            print(error)

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the stripped list?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clear the default stripped list instead")] = False           
    ):
    """
    Clears contents of the stripped list

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            values = _config.get_value(which_key(default))
            for value in values:
                removed = _config.remove_value(which_key(default), value)
                print(f"'{value}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}' list")
            print(f"The contents of '{which_key(default)}' was cleared")
        except KeyError as error:
            print(error)

@app.command()
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the stripped list with the default?", help="Force restore without confirmation")] = False):
    """
    Restores the stripped list to the default

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            blacklist_values = _config.get_value("stripped")
            for value in blacklist_values:
                removed = _config.remove_value("stripped", value)
                print(f"'{value}' {'was removed from the' if removed else 'does not exists in'} 'stripped' list")
            print(f"The contents of 'stripped' was cleared")
            default_values = _config.get_value("stripped_default")
            for value in default_values:
                added = _config.add_value("stripped", value)
                print(f"'{value}' {'was added to' if added else 'already exists in'} 'stripped'")
            print(f"The contents of 'stripped' have been restored")
        except KeyError as error:
            print(error)

@app.callback()
def stripped(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False):
    """
    Displays contents of the stripped list
    """
    if ctx.invoked_subcommand is None:
        try:
            print(_config.get_value(which_key(default)))
        except KeyError as error:
            print(error)
        
if __name__ == "__main__":
    app()