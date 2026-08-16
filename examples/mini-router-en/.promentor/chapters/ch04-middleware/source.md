# Source guide: middleware

## Core file: `mini_router/router.py:23-46` and `:88-107`

### Request / Response are the adapter protocol (:23-:46)

They are thin: method, path, params, body; status, body, headers. The router does not depend on `http.server`. Later, `server.py` only fills a `Request` from the stdlib and writes a `Response` back to the socket.

Keep the protocol in your own types so tests do not bind a port.

### `use` only registers (:88-:89)

The middleware list is ordered. `use` does not wrap — wrapping happens on every `handle`, so a middleware registered later applies to routes that already exist.

### `handle` wraps inside-out (:91-:107)

```
def leaf(req):
    result = handler(req)
    return result if isinstance(result, Response) else Response(200, str(result))

wrapped = leaf
for middleware in reversed(self._middleware):
    nxt = wrapped
    wrapped = lambda req, _mw=middleware, _nxt=nxt: _mw(req, _nxt)
return wrapped(request)
```

Three places to pause:

1. `reversed`: the first registered layer becomes the outermost.
2. `_mw=middleware, _nxt=nxt`: bind this iteration's values. `lambda req: middleware(req, wrapped)` makes every layer point at the last assignment.
3. 404 returns before the onion is wrapped. A miss does not run middleware — that is this course's contract, and the tests assert it.
