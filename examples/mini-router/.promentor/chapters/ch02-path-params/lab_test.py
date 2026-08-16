"""Black-box tests for :param matching."""

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


class PathParamTest(unittest.TestCase):
    def test_static_still_works(self):
        router = Router()
        users = _handler("users")
        router.add_route("GET", "/users", users)
        handler, params = router.find_route("GET", "/users")
        self.assertIs(handler, users)
        self.assertEqual(params, {})

    def test_param_route(self):
        router = Router()
        show = _handler("show")
        router.add_route("GET", "/users/:id", show)
        handler, params = router.find_route("GET", "/users/42")
        self.assertIs(handler, show)
        self.assertEqual(params, {"id": "42"})

    def test_nested_params(self):
        router = Router()
        show = _handler("show")
        router.add_route("GET", "/users/:uid/posts/:pid", show)
        handler, params = router.find_route("GET", "/users/1/posts/9")
        self.assertIs(handler, show)
        self.assertEqual(params, {"uid": "1", "pid": "9"})

    def test_param_method_mismatch(self):
        router = Router()
        router.add_route("GET", "/users/:id", _handler("show"))
        handler, params = router.find_route("POST", "/users/42")
        self.assertIsNone(handler)
        self.assertEqual(params, {})

    def test_wrong_length(self):
        router = Router()
        router.add_route("GET", "/users/:id", _handler("show"))
        handler, _ = router.find_route("GET", "/users/42/extra")
        self.assertIsNone(handler)

    def test_literal_segment_must_match(self):
        router = Router()
        router.add_route("GET", "/users/:id", _handler("show"))
        handler, _ = router.find_route("GET", "/posts/42")
        self.assertIsNone(handler)


if __name__ == "__main__":
    unittest.main()
