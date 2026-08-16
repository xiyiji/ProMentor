"""Provided HTTP adapter. Do not edit."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from router import Request, Router


def run(router: Router, host: str = "127.0.0.1", port: int = 8000) -> None:
    class Handler(BaseHTTPRequestHandler):
        def _dispatch(self) -> None:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode() if length else ""
            path = self.path.split("?", 1)[0]
            response = router.handle(Request(self.command, path, body=body))
            self.send_response(response.status)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.body.encode())

        def do_GET(self) -> None:
            self._dispatch()

        def do_POST(self) -> None:
            self._dispatch()

        def log_message(self, format: str, *args: object) -> None:
            return

    ThreadingHTTPServer((host, port), Handler).serve_forever()
