from dataclasses import dataclass
from typing import Iterable, Literal, TypeVar

from sirius.types import Message, Scope, Receive


Self = TypeVar("Self", bound="Request")


@dataclass
class ConnectionScope:
    type: Literal["http"]
    asgi_version: Literal["2.0", "2.1", "2.2", "2.3"]
    http_version: Literal["1.0", "1.1", "2.0"]
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    scheme: Literal["http", "https"]
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[list[bytes, bytes]]
    client: Iterable[str | int]
    server: Iterable[str | int | None]


@dataclass
class RequestReceive:
    type: Literal["http.request"]
    body: bytes
    more_body: bool


class Request:
    def __init__(self, scope: Scope, receive: Message) -> None:
        self.scope = ConnectionScope(
            type=scope.get("type", "http"),
            asgi_version=scope.get("asgi.version", "2.0"),
            http_version=scope.get("http.version"),
            method=scope.get("method"),
            scheme=scope.get("scheme", "http"),
            path=scope.get("path"),
            raw_path=scope.get("raw_path"),
            query_string=scope.get("query_string"),
            root_path=scope.get("root_path"),
            headers=scope.get("headers"),
            client=scope.get("client"),
            server=scope.get("server"),
        )
        self.receive = RequestReceive(
            type=receive.get("type"),
            body=receive.get("body"),
            more_body=receive.get("more_body"),
        )

    @classmethod
    async def from_request(cls: type[Self], scope: Scope, receive: Receive) -> Self:
        receive_body = b""
        more_body = True

        while more_body:
            message = await receive()
            receive_body += message.get("body", b"")
            more_body = message.get("more_body", False)

        receive_req = {
            "type": message.get("type"),
            "body": receive_body,
            "more_body": more_body,
        }

        return cls(scope, receive_req)
