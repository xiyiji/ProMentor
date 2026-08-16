# Source guide: static routes

## Core file: `mini_router/router.py:11-71`

### Splitting and normalizing (:11-:20)

`split_path` drops empty segments, so `/users/42/` and `/users/42` yield the same segments. `normalize_path` keeps the key stable: add a leading `/` if missing, strip the trailing slash, turn an empty path into `/`.

These look like helpers. They actually define equality for the routing table. If equality is fuzzy, every later lookup is wrong.

### Two tables, not one (:49-:55)

```
_static  : (METHOD, /path) → handler     # exact match
_dynamic : [(METHOD, segments, handler)] # unused in this chapter
```

The original design splits "O(1) is enough" from "must run a pattern matcher" at registration time. Put everything in a list and static routes become a linear scan too.

### Register: patterns go to the dynamic table (:57-:64)

`add_route` normalizes first, then checks whether any segment starts with `:` or `*`. Your implementation this chapter can be simpler: write only `_static`. Understand the fork anyway — it is why lookup can start with a dict get.

### Lookup: a static hit returns immediately (:66-:71)

```
static = self._static.get((method, path))
if static is not None:
    return static, {}
```

A static hit never enters the later loop. If `/users/new` exists next to `/users/:id`, the static table wins first. That is the root of chapter 3's priority rule.
