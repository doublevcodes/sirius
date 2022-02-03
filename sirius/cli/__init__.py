from pathlib import Path

import click
import uvicorn

from sirius import __version__
from sirius.config.config import DEFAULT_CONFIG_FILE_PATH
from sirius.config.export import export_default_config


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def main():
    ...


@main.command()
@click.argument(
    "file_name",
    default=DEFAULT_CONFIG_FILE_PATH,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=True,
        allow_dash=False,
        path_type=str,
    )
)
def export(file_name: str):
    export_default_config(Path(file_name))


@main.command()
@click.option("-p", "--port", help="Port to run the server on")
def dev(port: int):
    uvicorn.run("sirius.sirius:sirius", port=port, reload=True)
