"""Black-box tests for middleware onion and handle()."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Request, Response, Router  # noqa: E402


class MiddlewareTest(unittest.TestCase):
    def test_handle_invokes_handler(self):
        router = Router()
        router.add_route("GET", "/ping", lambda req: Response(200, "pong"))
        response = router.handle(Request("GET", "/ping"))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, "pong")

    def test_params_on_request(self):
        router = Router()
        router.add_route("GET", "/users/:id", lambda req: Response(200, req.params["id"]))
        response = router.handle(Request("GET", "/users/42"))
        self.assertEqual(response.body, "42")

    def test_not_found(self):
        router = Router()
        response = router.handle(Request("GET", "/missing"))
        self.assertEqual(response.status, 404)
        self.assertEqual(response.body, "not found")

    def test_not_found_skips_middleware(self):
        router = Router()
        calls = []

        def mark(request, nxt):
            calls.append("mw")
            return nxt(request)

        router.use(mark)
        response = router.handle(Request("GET", "/missing"))
        self.assertEqual(response.status, 404)
        self.assertEqual(calls, [])

    def test_onion_order(self):
        router = Router()
        order = []

        def outer(request, nxt):
            order.append("outer-in")
            response = nxt(request)
            order.append("outer-out")
            return response

        def inner(request, nxt):
            order.append("inner-in")
            response = nxt(request)
            order.append("inner-out")
            return response

        router.use(outer)
        router.use(inner)
        router.add_route(
            "GET",
            "/",
            lambda req: (order.append("handler") or Response(200, "ok")),
        )
        response = router.handle(Request("GET", "/"))
        self.assertEqual(response.body, "ok")
        self.assertEqual(
            order,
            ["outer-in", "inner-in", "handler", "inner-out", "outer-out"],
        )

    def test_middleware_can_short_circuit(self):
        router = Router()

        def deny(request, nxt):
            return Response(401, "no")

        router.use(deny)
        router.add_route("GET", "/secret", lambda req: Response(200, "yes"))
        response = router.handle(Request("GET", "/secret"))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.body, "no")


if __name__ == "__main__":
    unittest.main()
