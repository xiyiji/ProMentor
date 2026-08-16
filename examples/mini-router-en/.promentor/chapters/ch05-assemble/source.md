# Source guide: assemble

## Core files: `mini_router/demo.py:9-30` and `mini_router/server.py:10-32`

### An app is registration, not another router (demo.py:9-22)

`build_app` does three things: new Router, add_route, use. Handlers are lambdas that read `req.params` / `req.body`. Middleware mutates headers after the handler, so it must call `nxt(request)` first.

Your `app.py` should have the same shape. The only difference is imports from this chapter's `router` / `server`, not in-package relative paths.

### dispatch is a thin wrapper (demo.py:25-26)

One line: `router.handle(Request(...))`. Do not re-parse the path here. Parsing belongs to Router.

### HTTP adapter (server.py:10-32)

`Handler` closes over the outer `router`. `_dispatch` is the join point for every verb:

1. Read the body (no `Content-Length` means empty)
2. `path.split("?", 1)[0]` drops the query
3. `router.handle(Request(self.command, path, body=body))`
4. Write status, headers, and body

`log_message` is a no-op so the demo does not flood the terminal. That is not a design point.

The point: application code never subclasses `BaseHTTPRequestHandler`. Inheritance stays in the adapter.
