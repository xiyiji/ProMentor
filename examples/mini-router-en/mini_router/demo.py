"""A finished mini API assembled from Router + middleware."""

from __future__ import annotations

from .router import Request, Response, Router
from .server import run as serve


def build_app() -> Router:
    router = Router()
    router.add_route("GET", "/", lambda req: Response(200, "mini-router"))
    router.add_route("GET", "/users/:id", lambda req: Response(200, req.params["id"]))
    router.add_route("GET", "/files/*path", lambda req: Response(200, req.params["path"]))
    router.add_route("POST", "/echo", lambda req: Response(200, req.body))

    def logger(request: Request, nxt):
        response = nxt(request)
        response.headers.setdefault("X-Path", request.path)
        return response

    router.use(logger)
    return router


def dispatch(router: Router, method: str, path: str, body: str = "") -> Response:
    return router.handle(Request(method, path, body=body))


def run(router: Router, host: str = "127.0.0.1", port: int = 8000) -> None:
    serve(router, host, port)
