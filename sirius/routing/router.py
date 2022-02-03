import importlib
import json
import os
from pathlib import Path
from types import ModuleType
from typing import Callable
from urllib.parse import unquote_plus

from sirius.core.response import Response, ResponseBody, ResponseStart
from sirius.utils import METHODS, sentinel, _Sentinel, PATH_PARAMS_REGEX


def match_path(pattern, path):
    if pattern == path:
        return {}
    pattern_bits = pattern.strip("/").split("/")
    path_bits = path.strip("/").split("/")
    if len(pattern_bits) != len(path_bits):
        return False
    match = {}
    for pattern_bit, path_bit in zip(pattern_bits, path_bits):
        if pattern_bit.startswith("<") and pattern_bit.endswith(">"):
            name = pattern_bit[1:-1]
            match[name] = path_bit
        elif pattern_bit != path_bit:
            return False
    return match


class Router:
    """
    A router is responsible for dispatching requests to the appropriate route.
    """

    def __init__(self, routes_path: str) -> None:
        self.routes_path: str = routes_path
        self.route_folder: str = self.find_route_folder()

        self.routes: list[tuple[str, ModuleType]] = [
            (route, module) for (route, module) in self.process_routes()
        ]

        # This creates a dictionary, where the key is the route and the value is a dictionary of methods and their corresponding functions
        self.route_map: dict[str, dict[str, Callable | _Sentinel]] = {
            route[0]: {method.lower(): sentinel for method in METHODS}
            for route in self.routes
        }

        for route, module in self.routes:
            for method in [method.lower() for method in METHODS]:
                self.route_map[route][method] = getattr(module, method, sentinel)

    def find_route_folder(self) -> Path:
        route_folder = Path.cwd() / self.routes_path
        if route_folder.exists():
            return route_folder
        else:
            raise FileNotFoundError(
                f"Could not find {self.routes_path} folder in current working directory."
            )

    def process_routes(self):
        cwd = Path.cwd()
        python_files = [path for path in self.route_folder.rglob("*.py")]
        relative_routes = [str(path).removeprefix(str(cwd)) for path in python_files]

        path_module_path_pairs: list[tuple[str, str]] = []

        for file_route in relative_routes:
            route = file_route.removeprefix(f"{os.sep}{self.routes_path}")
            file_route = file_route.removesuffix(".py").replace(os.sep, ".")

            # __init__.py files represent root endpoints
            if route.endswith("__init__.py"):
                path_module_path_pairs.append(
                    (route.removesuffix("__init__.py"), file_route.removeprefix("."))
                )

            # Ignore endpoints prefixed with an underscore
            if route.startswith(f"{os.sep}_"):
                continue

            # All other files represent endpoints
            else:
                path_module_path_pairs.append(
                    (route.removesuffix(".py"), file_route.removeprefix("."))
                )

        path_module_pairs: list[tuple[str, ModuleType]] = [
            (path, importlib.import_module(module_path))
            for (path, module_path) in path_module_path_pairs
        ]
        return path_module_pairs

    def route(self, method: str, route: str, query: str) -> Response:

        if all(
            [match_path(pattern, route) is False for pattern in self.route_map.keys()]
        ):
            return Response(
                start=ResponseStart(
                    status=404,
                    headers=[
                        (b"Content-Type", b"text/plain"),
                        (b"Content-Length", b"0"),
                    ],
                )
            )

        for pattern in self.route_map.keys():
            if match_path(pattern, route) is not False:
                path = pattern
                path_params = match_path(pattern, route)
                break

        if method not in self.route_map[path]:
            raise KeyError(f"Method {method} not found")

        params: dict[str, str] = self.get_params(query)
        params: dict[str, str] = params | path_params

        route = self.route_map[pattern]
        function = route.get(method)
        function_annotations = function.__annotations__

        for param in params.keys():
            parameter = function_annotations.get(param, None)
            if parameter is None:
                raise KeyError(f"Parameter {param} not found")
            params[param] = parameter(params[param])

        response_body = function(**params)

        content_type = b"text/plain"
        status_code = 200

        match response_body:
            case str(response):
                response_body = response.encode("utf-8")
            case dict(response):
                content_type = b"application/json"
            case int(response):
                status_code = response
            case (str(response), int(code)):
                status_code = code
                response_body = response.encode("utf-8")
            case (dict(response), int(code)):
                content_type = b"application/json"
                status_code = code
                response_body = json.dumps(response).encode("utf-8")

        return Response(
            start=ResponseStart(
                status=status_code, headers=[(b"Content-Type", content_type)]
            ),
            body=ResponseBody(body=response_body, more_body=False),
        )

    def get_params(self, query) -> dict:
        query = unquote_plus(query.decode("utf-8"))

        params = query.split("&")
        if isinstance(params, str):
            params = [
                params,
            ]

        params = [param.split("=") for param in params if param != ""]

        return {param[0]: param[1] for param in params}
