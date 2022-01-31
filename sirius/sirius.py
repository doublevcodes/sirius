from dataclasses import asdict

from sirius.core import Request, Response
from sirius.routing import Router
from sirius.types import Scope, Receive, Send


class Sirius:
    def __init__(
        self,
        debug: bool | None = False,
    ) -> None:
        self._debug = debug
        self.router = Router("src/routes")  # TODO: when configuration is implemented, this should be a configurable value

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] == "http"

        request: Request = await Request.from_request(scope, receive)
        response = self.router.route(request.scope.path, request.scope.method.lower())
        await self.respond(send, response)

    async def respond(self, send: Send, response: Response) -> None:
        response = asdict(response)
        await send(response["start"])
        await send(response["body"])

    @property
    def debug(self) -> bool:
        return self._debug


sirius = Sirius()
