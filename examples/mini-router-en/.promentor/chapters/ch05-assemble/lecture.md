# Assemble a runnable Mini Router

This chapter wires the first four chapters into a tiny API you can actually run. When you finish, `python3 .promentor/main.py` should start a server — not just a pile of unit tests.

Where it sits: Router is the kernel. This chapter is the shell — register real routes and attach HTTP.

## The kernel already exists. Do not build another

`router.py` and `server.py` are the course-provided complete implementation (what you would have after chapters 1–4). **Do not edit them.** Your homework is only `app.py`: which URLs exist, what middleware does, and how one call becomes a `Response`.

Same as a real framework: you rarely rewrite the router. You write the app.

## build_app: the routing table is the product

Minimum set:

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/` | body is `mini-router` |
| GET | `/users/:id` | body is the id |
| GET | `/files/*path` | body is the remaining path |
| POST | `/echo` | body echoed back |

Then hang a logger: after calling `next`, set an `X-Path` header (the request path). That proves you wired middleware into the app, not only called `use` inside a test.

## dispatch: tests and HTTP share one path

```python
def dispatch(router, method, path, body=""):
    return router.handle(Request(method, path, body=body))
```

Tests go through `dispatch` and never bind a port. `run` hands the same `router` to `server.run`. Two doors, one kernel — otherwise you will spend a night on "tests pass, browser 404."

## What server.py does (read, do not write)

stdlib `BaseHTTPRequestHandler` splits verbs into `do_GET` / `do_POST`. The adapter folds them into one `router.handle(Request(...))` and writes the `Response` back. Drop the query string; read the body from `Content-Length`.

The router does not know HTTP. HTTP does not know the routing table. That is the boundary.

## What the lab asks for

In `app.py`, implement `build_app`, `dispatch`, and `run`. Signatures are in `lab.json`.

When you are done:

```bash
python3 .promentor/chapters/ch05-assemble/lab_test.py
python3 .promentor/main.py
```

Open `http://127.0.0.1:8000/` and you should see `mini-router`.
