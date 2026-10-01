from uuid import uuid4

from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        request_id = headers.get(REQUEST_ID_HEADER.lower().encode(), b"").decode() or str(uuid4())
        scope["soulos.request_id"] = request_id

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = list(message.get("headers", []))
                response_headers.append((REQUEST_ID_HEADER.lower().encode(), request_id.encode()))
                message = {**message, "headers": response_headers}
            await send(message)

        await self.app(scope, receive, send_with_request_id)
