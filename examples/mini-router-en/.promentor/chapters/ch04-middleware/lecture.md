# The middleware onion

This chapter pulls logging, auth, and header tweaks out of every handler and wraps them as layers of `next`.

Where it sits: `find_route` already found someone. `handle` builds the `Request`, wraps middleware, calls the handler, and returns 404 on a miss.

## Do not copy this into every handler

```python
def show_user(request):
    log(request)
    user = load(request.params["id"])
    log_done()
    return Response(200, user)
```

Three handlers means writing it three times. Miss one and "some endpoints have no logs." Cross-cutting concerns do not belong in business functions.

Shape of a middleware:

```python
def logger(request, nxt):
    response = nxt(request)
    response.headers["X-Path"] = request.path
    return response
```

It receives `next`, decides when to call it, and may short-circuit (`return Response(401)` on a failed auth).

## Onion: register forward, wrap backward

After `use(A); use(B)`, one request runs:

```text
A enter → B enter → handler → B leave → A leave
```

Implementation: wrap outward from the handler. Start with `wrapped = handler`, then `for mw in reversed(middleware): wrapped = lambda req: mw(req, wrapped)`.

A forward `for` puts B on the outside, and log/auth order flips. The closure must bind the current `mw` and `nxt` as default arguments, or every layer points at the last loop value.

## handle is the only entry

`find_route` only answers "who, and with what params." `handle` is what runs:

1. Look up
2. Write params onto `request.params`
3. No handler → `Response(404, "not found")`, do not raise
4. If the handler returns a plain value, wrap it as `Response(200, str(value))`
5. Wrap middleware, then call

404 is still a response. The caller (next chapter's HTTP adapter) only speaks `Response`.

## What the lab asks for

`Request` / `Response` are already in the stub. Do not rename fields.

You implement:

- `use(middleware)`: register in call order
- `handle(request)`: lookup + onion + 404

Keep using your own `find_route`. Tests check middleware order, that params land on the request, and that a miss is 404.
