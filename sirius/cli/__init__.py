from pathlib import Path
from typing import Optional

import attr
import click
import uvicorn

from sirius import __version__
from sirius.config.config import DEFAULT_CONFIG_FILE_PATH, update_config, get_config
from sirius.config.export import export_default_config


def parse_config(
    ctx: click.Context, _param: click.Parameter, value: Optional[str]
) -> Optional[str]:
    config_file = value or DEFAULT_CONFIG_FILE_PATH
    update_config(config_file)
    config = attr.asdict(get_config().user)

    if ctx.default_map:
        ctx.default_map.update(config)
    else:
        ctx.default_map = config

    return config_file


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    is_eager=True,
    callback=parse_config,
    help="Read configuration from FILE path.",
)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context, config: str, verbose: bool) -> None:
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
    ),
)
@click.pass_context
def export(ctx: click.Context, file_name: str) -> None:
    export_default_config(Path(file_name))


@main.command()
@click.option("-p", "--port", help="Port to run the server on", type=int)
@click.pass_context
def dev(ctx: click.Context, port: int) -> None:
    uvicorn.run("sirius.sirius:sirius", port=port, reload=True)
