import typer
from rich import print
from typing_extensions import Annotated

import _config

which_key = lambda default: "blacklist_default" if default else "blacklist"

app = typer.Typer()

@app.command()
def add(
        words: Annotated[list[str], typer.Argument(help="The word(s) to be added to the blacklist")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add word(s) to the default blacklist instead")] = False
    ):
    """
    Add a word(s) to the blacklist
    """
    for word in words:
        try:
            added: bool = _config.add_value(which_key(default), word)
            print(f"'{word}' {'was added to the' if added else 'already exists in the'} '{which_key(default)}'")
        except KeyError as error:
            print(error)
                
@app.command()
def remove(
        words: Annotated[list[str], typer.Argument(help="The word(s) to be removed from the blacklist")],
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of the default blacklist instead")] = False
    ):
    """
    Remove a word(s) from the blacklist
    """
    for word in words:
        try:
            removed: bool = _config.remove_value(which_key(default), word)
            print(f"'{word}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}'")
        except KeyError as error:
            print(error)

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the blacklist?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clears the default blacklist instead")] = False           
    ):
    """
    Clears contents of the blacklist

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            values: str | list[str] = _config.get_value(which_key(default))
            for value in values:
                removed: bool = _config.remove_value(which_key(default), value)
                print(f"'{value}' {'was removed from' if removed else 'does not exists in'} '{which_key(default)}'")
            print(f"The contents of '{which_key(default)}' was cleared")
        except KeyError as error:
            print(error)

@app.command()
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the blacklist with the contents of the default blacklist?", help="Force restore without confirmation")] = False):
    """
    Restores blacklist to the default blacklist

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            blacklist_values: str | list[str] = _config.get_value("blacklist")
            for value in blacklist_values:
                removed: bool = _config.remove_value("blacklist", value)
                print(f"'{value}' {'was removed from the' if removed else 'does not exists in the'} 'blacklist'")
            print(f"The contents of 'blacklist' was cleared")
            default_values: str | list[str] = _config.get_value("blacklist_default")
            for value in default_values:
                added: bool = _config.add_value("blacklist", value)
                print(f"'{value}' {'was added to the' if added else 'already exists in the'} 'blacklist'")
            print(f"The contents of 'blacklist' have been restored")
        except KeyError as error:
            print(error)

@app.callback()
def blacklist(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of the default blacklist instead")] = False):
    """
    Displays the contents of the blacklist
    """
    if ctx.invoked_subcommand is None:
        try:
            print(_config.get_value(which_key(default)))
        except KeyError as error:
            print(error)
            
if __name__ == "__main__":
    app()