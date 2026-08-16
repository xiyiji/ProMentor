"""Black-box tests for match priority and wildcards."""

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


class PriorityWildcardTest(unittest.TestCase):
    def test_static_beats_param(self):
        router = Router()
        create = _handler("create")
        show = _handler("show")
        router.add_route("GET", "/users/:id", show)
        router.add_route("GET", "/users/new", create)
        handler, params = router.find_route("GET", "/users/new")
        self.assertIs(handler, create)
        self.assertEqual(params, {})

    def test_param_still_matches_other_ids(self):
        router = Router()
        create = _handler("create")
        show = _handler("show")
        router.add_route("GET", "/users/:id", show)
        router.add_route("GET", "/users/new", create)
        handler, params = router.find_route("GET", "/users/42")
        self.assertIs(handler, show)
        self.assertEqual(params, {"id": "42"})

    def test_param_beats_wildcard(self):
        router = Router()
        show = _handler("show")
        rest = _handler("rest")
        router.add_route("GET", "/users/*rest", rest)
        router.add_route("GET", "/users/:id", show)
        handler, params = router.find_route("GET", "/users/42")
        self.assertIs(handler, show)
        self.assertEqual(params, {"id": "42"})

    def test_wildcard_captures_remainder(self):
        router = Router()
        files = _handler("files")
        router.add_route("GET", "/files/*path", files)
        handler, params = router.find_route("GET", "/files/a/b/c")
        self.assertIs(handler, files)
        self.assertEqual(params, {"path": "a/b/c"})

    def test_wildcard_empty_remainder(self):
        router = Router()
        files = _handler("files")
        router.add_route("GET", "/files/*path", files)
        handler, params = router.find_route("GET", "/files")
        self.assertIs(handler, files)
        self.assertEqual(params, {"path": ""})

    def test_method_still_matters(self):
        router = Router()
        router.add_route("GET", "/files/*path", _handler("files"))
        handler, _ = router.find_route("POST", "/files/a")
        self.assertIsNone(handler)


if __name__ == "__main__":
    unittest.main()
