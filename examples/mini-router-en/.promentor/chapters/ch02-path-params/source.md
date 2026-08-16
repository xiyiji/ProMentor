# Source guide: path parameters

## Core file: `mini_router/router.py:11-13`, `:57-64`, and `:110-125`

### Why split first (:11-:13)

`split_path` is the precondition for param matching. The string `/users/:id` cannot be compared to `/users/42`. After the split, the unit of comparison is "is this cell a literal or a rule?"

### Split at registration (:57-:64)

```
if any(seg.startswith(":") or seg.startswith("*") for seg in segments):
    self._dynamic.append((method, segments, handler))
    return
self._static[(method, path)] = handler
```

The dynamic table stores already-split `segments`, so lookup does not re-split the template. `:` and `*` are prefix markers, not regex — the router defines its own grammar. You do not hand the path to a regex engine.

### `_match`: the rule interpreter (:110-:125)

Per segment:

1. Starts with `*`: swallow the rest of the request (next chapter; you may ignore it here)
2. Ran out of request segments: fail
3. Starts with `:`: `params[name] = request[index]`
4. Otherwise the literals must be equal
5. After the pattern is consumed, the request must be consumed too

Step 5 matters. Without it, `/users/:id` will incorrectly eat `/users/42/extra`.

You write steps 3, 4, and 5 yourself. Do not `==` against `:id`.
