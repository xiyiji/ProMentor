"""Black-box tests for the assembled demo app."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import build_app, dispatch  # noqa: E402


class AssembleTest(unittest.TestCase):
    def setUp(self):
        self.router = build_app()

    def test_home(self):
        response = dispatch(self.router, "GET", "/")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, "mini-router")

    def test_user_param(self):
        response = dispatch(self.router, "GET", "/users/42")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, "42")

    def test_wildcard_file(self):
        response = dispatch(self.router, "GET", "/files/a/b/c")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, "a/b/c")

    def test_echo(self):
        response = dispatch(self.router, "POST", "/echo", body="hello")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, "hello")

    def test_logger_sets_path_header(self):
        response = dispatch(self.router, "GET", "/")
        self.assertEqual(response.headers.get("X-Path"), "/")

    def test_unknown_is_404(self):
        response = dispatch(self.router, "GET", "/nope")
        self.assertEqual(response.status, 404)


if __name__ == "__main__":
    unittest.main()
