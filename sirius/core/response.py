from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class ResponseStart:
    type: bytes = "http.response.start"
    status: int = 200
    headers: Iterable[tuple[bytes, bytes]] = field(default_factory=list)


@dataclass
class ResponseBody:
    type: bytes = "http.response.body"
    body: bytes = b""
    more_body: bool = False


@dataclass
class Response:
    start: ResponseStart
    body: ResponseBody
