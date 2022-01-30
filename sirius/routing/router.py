from pathlib import Path


def find_route_folder():
    cwd = Path.cwd()
    route_folder = cwd / "src" / "routes"
    if route_folder.exists():
        return route_folder
    else:
        raise FileNotFoundError(f"Could not find src/routes folder in {cwd}")


class Router:
    def __init__(self) -> None:
        route_folder = find_route_folder()
        routes = [path.stem for path in route_folder.rglob("*.py")]
