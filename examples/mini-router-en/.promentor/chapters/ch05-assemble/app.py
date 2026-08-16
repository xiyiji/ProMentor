"""Ch05 lab: assemble the demo API. Do not import mini_router."""

from router import Request, Response, Router
from server import run as serve


def build_app() -> Router:
    return Router()


def dispatch(router: Router, method: str, path: str, body: str = "") -> Response:
    return Response(500, "not implemented")


def run(router: Router, host: str = "127.0.0.1", port: int = 8000) -> None:
    serve(router, host, port)
