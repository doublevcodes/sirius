from dataclasses import dataclass
from typing import Iterable, Literal, TypeVar

from sirius.types import Message, Scope, Receive


Self = TypeVar("Self", bound="Request")


@dataclass
class ConnectionScope:
    """This is a dataclass representing the scope of a connection request.

    :param scope: The scope of the connection request.
    """
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
            type=scope.pop("type", "http"),
            asgi_version=scope.pop("asgi.version", "2.0"),
            http_version=scope.pop("http.version"),
            method=scope.pop("method"),
            scheme=scope.pop("scheme", "http"),
            **scope,
        )
        self.receive = RequestReceive(
            **receive,
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
