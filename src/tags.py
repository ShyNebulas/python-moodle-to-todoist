import typer
from rich import print
from typing_extensions import Annotated

import _config

which_key = lambda default: "tags_default" if default else "tags"

app = typer.Typer()

@app.command()
def add(
        tag: Annotated[tuple[str, str], typer.Argument(help="The tag to be added to the tags list")], 
        default: Annotated[bool, typer.Option("--default", "-d", help="Add tag to the default tag list instead")] = False
    ):
    """
    Add a tag to the tag list
    """
    try:
        added: bool = _config.add_value(which_key(default), tag)
        print(f"'{tag}' {'was added to the' if added else 'already exists in the'} '{which_key(default)}'")
    except KeyError as error:
        print(error)

@app.command()
def remove(
        key: Annotated[str, typer.Argument(help="The key to be removed from the tag list")] = None,
        default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default tag list instead")] = False
    ):
    """
    Remove a key, and it's pair, from the tag list
    """
    try:
        removed: bool = _config.remove_value(which_key(default), ((key),))
        print(f"'{key}' {'was removed from the' if removed else 'does not exists in the'} '{which_key(default)}'")
    except KeyError as error:
        print(error)

@app.command()
def remove_all(
        force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to clear the tag list?", help="Force deletion without confirmation")] = False,
        default: Annotated[bool, typer.Option("--default", "-d", help="Clear the default tag list instead")] = False           
    ):
    """
    Clears contents of the tag list

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
def restore(force: Annotated[bool, typer.Option("--force", "-f", prompt="Are you sure you want to restore the tag list with the default tag list?", help="Force restore without confirmation")] = False):
    """
    Restores tag list to the default

    If --force/-f is not used, will ask for confirmation.
    """
    if force:
        try:
            tag_dict: dict = _config.get_value("tags")
            for key in tag_dict:
                removed: bool = _config.remove_value("tags", ((key),))
                print(f"'{key}' {'was removed from the' if removed else 'does not exists in the'} 'tags'")
            print(f"The contents of 'tags' was cleared")
            default_dict: dict = _config.get_value("tags_default")
            for key in default_dict:
                added: bool = _config.add_value("tags", (key, default_dict[key]))
                print(f"'{key}' {'was added to the' if added else 'already exists in the'} 'tags'")
            print(f"The contents of 'tags' have been restored")
        except KeyError as error:
            print(error)

@app.callback()
def tags(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", "-d", help="Shows the contents of default instead")] = False):
    """
    Displays contents of the tag list
    """
    if ctx.invoked_subcommand is None:
        try:
            print(_config.get_value(which_key(default)))
        except KeyError as error:
            print(error)
        
if __name__ == "__main__":
    app()