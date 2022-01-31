import argparse
import uvicorn

cli = argparse.ArgumentParser(description="A CLI for Sirius projects.", add_help=True)

subparsers = cli.add_subparsers(dest="subcommand")


def subcommand(args=[], parent=subparsers):
    def decorator(func):
        parser = parent.add_parser(func.__name__, help=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


def argument(*name_or_flags, **kwargs):
    return ([*name_or_flags], kwargs)


@subcommand([argument("-p", "--port", help="Port to run the server on")])
def dev(args):
    uvicorn.run("sirius.sirius:sirius", port=int(args.port) if args.port else 8000, reload=True)


def main():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
