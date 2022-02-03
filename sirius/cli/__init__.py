import click
import uvicorn

from sirius import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def main():
    ...


@main.command()
@click.option("-p", "--port", help="Port to run the server on")
def dev(args):
    uvicorn.run(
        "sirius.sirius:sirius", port=int(args.port) if args.port else 8000, reload=True
    )
