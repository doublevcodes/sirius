import importlib
import json
import os
from pathlib import Path
from types import ModuleType
from typing import Callable

from sirius.core.response import Response, ResponseBody, ResponseStart
from sirius.utils import METHODS, sentinel, _Sentinel


class Router:
    def __init__(self, routes_path: str) -> None:
        self.routes_path = routes_path
        self.route_folder = self.find_route_folder()

        self.routes = [
            (route, module)
            for (route, module)
            in self.process_routes()
        ]

        self.route_map: dict[str, dict[str, Callable | _Sentinel]] = {
            route[0]: {
                method.lower(): sentinel
                for method
                in METHODS
            }
            for route
            in self.routes
        }

        for route, module in self.routes:
            for method in [method.lower() for method in METHODS]:
                if hasattr(module, method):
                    self.route_map[route][method] = getattr(module, method)

    def find_route_folder(self) -> Path:
        route_folder = Path.cwd() / self.routes_path
        if route_folder.exists():
            return route_folder
        else:
            raise FileNotFoundError(f"Could not find {self.routes_path} folder in current working directory.")

    def process_routes(self):
        cwd = Path.cwd()
        python_files = [path for path in self.route_folder.rglob("*.py")]
        relative_routes = [str(path).removeprefix(str(cwd)) for path in python_files]

        path_module_path_pairs: list[tuple[str, str]] = []

        for file_route in relative_routes:
            route = file_route.removeprefix(f"{os.sep}{self.routes_path}")
            file_route = file_route.removesuffix(".py").replace(os.sep, ".")

            if route.startswith(f"{os.sep}_"):
                continue

            if route.endswith("__init__.py"):
                path_module_path_pairs.append((route.removesuffix("index.py"), file_route.removeprefix(".")))

            else:
                path_module_path_pairs.append((route.removesuffix(".py"), file_route.removeprefix(".")))

        path_module_pairs: list[tuple[str, ModuleType]] = [(path, importlib.import_module(module_path)) for (path, module_path) in path_module_path_pairs]
        return path_module_pairs

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
