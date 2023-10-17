import typer
from rich import print
from rich.panel import Panel
from todoist_api_python.api import TodoistAPI
from pathlib import Path
from typing_extensions import Annotated

from bs4 import Tag

import _config
import soup
import directory

app = typer.Typer()

@app.command()
def folder(path: Annotated[Path, typer.Argument(help="The folder path to be set")]):
    """
    Setting folder path
    """
    try:
        added: bool = _config.add_value("folder", path)
        print(f"'{path}' {'was added to the' if added else 'already exists in'} 'folder'")
    except KeyError as error:
        print(error)

@app.callback()
def run(
        ctx: typer.Context,
        ignore_blacklist: Annotated[bool, typer.Option("--ignore-blacklist", "-ib", help="Ignores the blacklist when running")] = False,
        ignore_stripped: Annotated[bool, typer.Option("--ignore-stripped", "-is", help="Ignores the stripped list when running")] = False,
        ignore_clean: Annotated[bool, typer.Option("--ignore-clean", "-ic", help="Ignores cleaning each instance when running")] = False
    ):
    if ctx.invoked_subcommand is None:
        try:
            todoist_key: str = _config.get_value("todoist_key")
            if not todoist_key:
                print("'todoist_key' not set")
                raise typer.Exit(code=1)
            api = TodoistAPI(todoist_key)
            folder_path: str = _config.get_value("folder")
            if not folder_path:
                print("'folder' path not set")
                raise typer.Exit(code=1)
            htmls: list[Path] = directory.get_dirs_valid_htmls(Path(folder_path))
            pair_list: list[tuple[str, dict[str, str]]] = []
            for html in htmls:
                sections: list[Tag] = soup.get_raw_html_sections(html)
                if not sections: 
                    print(f"{html} has no valid sections")
                    continue
                pairs: dict[str, str] = {}
                for section in sections:
                    header: Tag = soup.get_raw_header(section)
                    if header:
                        if not soup.is_instance_blacklisted(header) or ignore_blacklist:
                            title_stripped: str = soup.strip_instance(header) if not ignore_stripped else header.text
                            title_clean: str = soup.clean_instance(title_stripped) if not ignore_clean else title_stripped
                            items: list[Tag] = soup.get_raw_instances_from_section(section)
                            items_string = ""
                            for item in items:
                                item_stripped: str = soup.strip_instance(item) if not ignore_stripped else item.text
                                item_clean: str = soup.clean_instance(item_stripped) if not ignore_clean else item_stripped
                                items_string += f"{item_clean}\n"
                            if items_string:
                                pairs[title_clean] = items_string
                print(Panel(soup.get_panel(pairs), title=soup.get_html_class(html)))
                pair_list.append((html, pairs))
            confirm: bool = typer.confirm("Add to todoist")
            if confirm:
                for html in pair_list:
                    title: str = html[0]
                    pairs: dict[str, str] = html[1]
                    klass: str = soup.get_html_class(html)
                    projects: dict[str, str] = _config.get_value("projects")
                    if klass.lower() not in projects:
                        print(f"{klass} has no 'project' key set")
                        raise typer.Exit(code=1)
                    project = projects[klass.lower()]
                    for title, content in pairs.items():
                        section = api.add_section(project_id = project, name=title)
                        for task in content.splitlines():
                            api.add_task(
                                project_id = project,
                                section_id = section.id,
                                content = task
                            )
                            print(f"Added '{task}' to '{section.name}'")
        except (NotADirectoryError, KeyError) as error:
            print(error)


