from typing import Callable, Sequence

from sirius.core import Request
from sirius.routing import Router, Route
from sirius.types import Scope, Receive, Send


class Sirius:
    def __init__(
        self,
        debug: bool | None = False,
        up: Sequence[Callable] = [],
        down: Sequence[Callable] = [],
    ) -> None:
        self._debug = debug
        self.router = Router()
        self.up = up
        self.down = down

        for up_fn in self.up:
            up_fn()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "http"

        request: Request = await Request.from_request(scope, receive)
        body = f"Received {request.scope.method} {request.scope.path}"
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )
        await send({"type": "http.response.body", "body": body.encode("utf-8")})

    def __del__(self) -> None:
        for down_fn in self.down:
            down_fn()

    @property
    def debug(self) -> bool:
        return self._debug


sirius = Sirius(up=[lambda: print("Up")], down=[lambda: print("Down")])
