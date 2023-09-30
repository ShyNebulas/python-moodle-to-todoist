from rich.console import Console
from rich.theme import Theme

themes = Theme({
    "warning": "bold dark_orange",
    "failure": "bold red1"
})

console = Console(theme=themes)