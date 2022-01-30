import importlib
import json
from pathlib import Path

from sirius.core.response import Response, ResponseBody, ResponseStart
from sirius.utils import sentinel


METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"]


def find_route_folder():
    cwd = Path.cwd()
    route_folder = cwd / "src" / "routes"
    if route_folder.exists():
        return route_folder
    else:
        raise FileNotFoundError(f"Could not find src/routes folder in {cwd}")


def route_processing_pipeline(routes: list[str]):
    for file_route in routes:
        route = file_route.removeprefix("/src/routes")
        if route.endswith("__init__.py"):
            continue
        if route.endswith("index.py"):
            yield route.removesuffix("index.py"), file_route.removeprefix("/").replace(
                "/", "."
            ).removesuffix(".py")
        else:
            yield route.removesuffix(".py"), file_route.removeprefix("/").replace(
                "/", "."
            ).removesuffix(".py")


class Router:
    def __init__(self) -> None:
        cwd = Path.cwd()
        route_folder = find_route_folder()
        routes = [path for path in route_folder.rglob("*.py")]
        unprocessed_routes = [str(path).removeprefix(str(cwd)) for path in routes]
        self.routes = [
            (route, module_path)
            for (route, module_path) in route_processing_pipeline(unprocessed_routes)
        ]

        self.route_map = {
            route[0]: {
                "get": sentinel,
                "post": sentinel,
                "put": sentinel,
                "delete": sentinel,
                "head": sentinel,
                "options": sentinel,
                "trace": sentinel,
            }
            for route in self.routes
        }

        for route, module_name in self.routes:
            loaded_route = importlib.import_module(module_name)
            for method in [method.lower() for method in METHODS]:
                if hasattr(loaded_route, method):
                    self.route_map[route][method] = getattr(loaded_route, method)

    def route(self, route: str, method: str) -> Response:
        if route not in self.route_map:
            raise KeyError(f"Route {route} not found")
        if method not in self.route_map[route]:
            raise KeyError(f"Method {method} not found")
        response_body = self.route_map[route][method]()

        content_type = b"text/plain"
        status_code = 200

        if isinstance(response_body, str):
            response_body = response_body.encode("utf-8")
            content_type = b"text/plain"
        elif isinstance(response_body, bytes):
            content_type = b"text/plain"
        elif isinstance(response_body, dict):
            response_body = bytes(json.dumps(response_body), "utf-8")
            content_type = b"application/json"
        elif isinstance(response_body, int):
            status_code = response_body
        elif isinstance(response_body, tuple):
            if len(response_body) == 2:
                response_body, status_code = response_body
            elif len(response_body) == 3:
                response_body, status_code, content_type = response_body
            if isinstance(response_body, str):
                response_body = response_body.encode("utf-8")
            elif isinstance(response_body, dict):
                response_body = bytes(json.dumps(response_body), "utf-8")
                content_type = b"application/json"
        else:
            raise ValueError(f"Invalid response body {response_body}")

        return Response(
            start=ResponseStart(
                status=status_code, headers=[(b"Content-Type", content_type)]
            ),
            body=ResponseBody(body=response_body, more_body=False),
        )
