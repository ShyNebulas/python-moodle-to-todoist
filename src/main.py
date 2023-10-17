import typer

import config
import run

app = typer.Typer()

app.add_typer(config.app, name="config")
app.add_typer(run.app, name="run", invoke_without_command=True)

if __name__ == "__main__":
    app()