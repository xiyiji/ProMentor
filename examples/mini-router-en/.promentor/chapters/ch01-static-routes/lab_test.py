"""Black-box tests for static route matching."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import Router  # noqa: E402


def _handler(name):
    def inner(*_args, **_kwargs):
        return name

    inner.__name__ = name
    return inner


class StaticRouteTest(unittest.TestCase):
    def test_static_route(self):
        router = Router()
        users = _handler("users")
        router.add_route("GET", "/users", users)
        handler, params = router.find_route("GET", "/users")
        self.assertIs(handler, users)
        self.assertEqual(params, {})

    def test_method_mismatch(self):
        router = Router()
        router.add_route("GET", "/users", _handler("users"))
        handler, params = router.find_route("POST", "/users")
        self.assertIsNone(handler)
        self.assertEqual(params, {})

    def test_missing_route(self):
        router = Router()
        router.add_route("GET", "/users", _handler("users"))
        handler, _ = router.find_route("GET", "/posts")
        self.assertIsNone(handler)

    def test_trailing_slash(self):
        router = Router()
        users = _handler("users")
        router.add_route("GET", "/users/", users)
        handler, _ = router.find_route("GET", "/users")
        self.assertIs(handler, users)

    def test_method_case(self):
        router = Router()
        users = _handler("users")
        router.add_route("get", "/users", users)
        handler, _ = router.find_route("GET", "/users")
        self.assertIs(handler, users)

    def test_root(self):
        router = Router()
        home = _handler("home")
        router.add_route("GET", "/", home)
        handler, _ = router.find_route("GET", "/")
        self.assertIs(handler, home)


if __name__ == "__main__":
    unittest.main()
