"""HTTP router: static paths, :params, *wildcards, and middleware."""

from __future__ import annotations

from typing import Any, Callable

Handler = Callable[..., Any]
Middleware = Callable[[Any, Callable[[Any], Any]], Any]


def split_path(path: str) -> list[str]:
    """Turn `/users/42/` into `['users', '42']`. Root becomes `[]`."""
    return [seg for seg in path.split("/") if seg]


def normalize_path(path: str) -> str:
    """`/users/` and `/users` are the same route. Empty path is `/`."""
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/") or "/"


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
        # Exact lookup: O(1) for routes with no :param or *wildcard.
        self._static: dict[tuple[str, str], Handler] = {}
        # Pattern routes, tried only after a static miss.
        self._dynamic: list[tuple[str, list[str], Handler]] = []
        self._middleware: list[Middleware] = []

    def add_route(self, method: str, path: str, handler: Handler) -> None:
        method = method.upper()
        path = normalize_path(path)
        segments = split_path(path)
        if any(seg.startswith(":") or seg.startswith("*") for seg in segments):
            self._dynamic.append((method, segments, handler))
            return
        self._static[(method, path)] = handler

    def find_route(self, method: str, path: str) -> tuple[Handler | None, dict[str, str]]:
        method = method.upper()
        path = normalize_path(path)
        static = self._static.get((method, path))
        if static is not None:
            return static, {}

        request_segs = split_path(path)
        best: tuple[int, Handler, dict[str, str]] | None = None
        for route_method, segments, handler in self._dynamic:
            if route_method != method:
                continue
            params = _match(segments, request_segs)
            if params is None:
                continue
            score = _specificity(segments)
            if best is None or score > best[0]:
                best = (score, handler, params)
        if best is None:
            return None, {}
        return best[1], best[2]

    def use(self, middleware: Middleware) -> None:
        self._middleware.append(middleware)

    def handle(self, request: Request) -> Response:
        handler, params = self.find_route(request.method, request.path)
        request.params = params
        if handler is None:
            return Response(404, "not found")

        def leaf(req: Request) -> Response:
            result = handler(req)
            if isinstance(result, Response):
                return result
            return Response(200, str(result))

        wrapped: Callable[[Request], Response] = leaf
        for middleware in reversed(self._middleware):
            nxt = wrapped
            wrapped = lambda req, _mw=middleware, _nxt=nxt: _mw(req, _nxt)
        return wrapped(request)


def _match(pattern: list[str], request: list[str]) -> dict[str, str] | None:
    params: dict[str, str] = {}
    for index, seg in enumerate(pattern):
        if seg.startswith("*"):
            name = seg[1:] or "path"
            params[name] = "/".join(request[index:])
            return params
        if index >= len(request):
            return None
        if seg.startswith(":"):
            params[seg[1:]] = request[index]
        elif seg != request[index]:
            return None
    if len(request) != len(pattern):
        return None
    return params


def _specificity(pattern: list[str]) -> int:
    # Static beats :param beats *wildcard, so /users/new wins over /users/:id.
    score = 0
    for seg in pattern:
        if seg.startswith("*"):
            score += 1
        elif seg.startswith(":"):
            score += 2
        else:
            score += 4
    return score
