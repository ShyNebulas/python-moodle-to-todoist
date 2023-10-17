from rich.console import group
from rich.panel import Panel
from pathlib import Path
from bs4 import BeautifulSoup, Tag
import re

import _config

def get_html_class(path: Path) -> str:
    return re.findall(r"(CS\d+)", str(path))[0]

def get_raw_html_sections(path: Path) -> list[Tag]:
    if not path.suffix == ".html": raise Exception(f"{path} is not an HTML file") 
    if path.stat().st_size == 0: raise Exception(f"{path} is empty")
    with path.open(mode="r+", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        sections: list[Tag] = [section for section in soup.select(".content")]
        return sections
    
def get_raw_header(sections: list[Tag]) -> Tag:
    header: list[Tag] = sections.select(".sectionname")
    return header[0] if header else None

def get_raw_instances_from_section(section: Tag) -> list[Tag]:
    instances: list[Tag] = [instance for instance in section.select(".instancename")]
    return instances

#TODO: Probably a better way to do this
def is_instance_blacklisted(instance: Tag) -> bool:
    for term in _config.get_value("blacklist"):
        if re.search(rf"\b({term})\b".format(term), instance.text, flags=re.IGNORECASE):
            return True
    return False

#TODO: Probably a better way to do this
def clean_instance(instance: str) -> str:
    leading: str = instance.lstrip("0123456789.- ")
    brackets: str = re.sub("[\(\[].*?[\)\]]", "", leading)
    split: list[str] = re.findall(r"[\w']+", brackets)
    joined: str = " ".join(split)
    trailing: str = joined.rstrip("0123456789.- ")
    return trailing

def strip_instance(instance: Tag) -> str:
    try:
        result: str = instance.text
        for word in _config.get_value("stripped"):
            pattern: re.Pattern = re.compile(f"(\s*){word}(\s*)", re.IGNORECASE)
            result: str = pattern.sub("", result)
        return result
    except KeyError:
        raise

@group()
def get_panel(pairs: dict[str, str]) -> Panel:
    for title, contents in pairs.items():
        yield Panel(contents, title=title)
    









    

    

                  
                  
              
      