"""Ch04 lab: keep routing, add middleware onion + handle()."""

from __future__ import annotations


class Request:
    def __init__(
        self,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        body: str = "",
    ) -> None:
        self.method = method.upper()
        self.path = path
        self.params = params or {}
        self.body = body


class Response:
    def __init__(
        self,
        status: int = 200,
        body: str = "",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status = status
        self.body = body
        self.headers = headers or {"Content-Type": "text/plain; charset=utf-8"}


class Router:
    def __init__(self) -> None:
        pass

    def add_route(self, method: str, path: str, handler) -> None:
        pass

    def find_route(self, method: str, path: str):
        return None, {}

    def use(self, middleware) -> None:
        pass

    def handle(self, request: Request) -> Response:
        return Response(500, "not implemented")
