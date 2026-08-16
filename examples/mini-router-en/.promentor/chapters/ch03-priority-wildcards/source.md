# Source guide: priority and wildcards

## Core file: `mini_router/router.py:66-86` and `:110-138`

### Lookup picks the most specific match, not the first (:66-:86)

After the static get, the dynamic table scans every template with the same method that `_match` accepts, and updates `best` with `_specificity`. Replace only when `score > best[0]` — a tie keeps the first match.

There is no early `return`. The first dynamic route that matches is not necessarily the right one.

### Wildcards inside `_match` (:112-:116)

```
if seg.startswith("*"):
    name = seg[1:] or "path"
    params[name] = "/".join(request[index:])
    return params
```

A wildcard returns immediately: the remaining segments (possibly empty) belong to it. So `/files/*path` against `/files/` (normalized to `['files']`) yields `path=""`.

### Scoring (:128-:138)

The 4 / 2 / 1 gaps guarantee that one extra static segment always beats "one fewer static, one more param." You may use other positive numbers as long as the order is the same: static > param > wildcard.

Do not disambiguate by hard-coding special paths. A score is the rule that scales.
