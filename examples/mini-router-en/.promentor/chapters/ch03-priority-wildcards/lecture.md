# Priority and wildcards

This chapter is about who wins when routes collide, and how `*path` eats the rest of the path. It is the easiest layer to get wrong, and the one that most shows the design.

Where it sits: dynamic matching no longer returns "the first hit." It returns the **most specific** hit.

## Collision is the normal case

Register both:

```text
GET /users/new
GET /users/:id
```

`GET /users/new` can be read two ways: the literal `new`, or `new` as an id.

If "first registered wins," the winner depends on add order, and the API silently changes when you reorder registrations. The rule must be order-independent: **static segment > param segment > wildcard**.

## Specificity, not if/else patches

Do not write:

```python
if path == "/users/new":
    ...
elif looks_like_id(path):
    ...
```

Every special path adds a branch. The original design scores the template:

| Segment kind | Score |
|--------------|-------|
| static `users` | 4 |
| param `:id` | 2 |
| wildcard `*path` | 1 |

`/users/new` scores 8, `/users/:id` scores 6. Higher wins. On a tie, keep the first scanned — tests do not depend on a tie-break beyond that.

The static table is still checked first. If `/users/new` was registered as a static route, it never enters the scoring loop. That is the real use of chapter 1's "static hit returns immediately."

## Wildcards eat the remainder

`/files/*path` against `/files/a/b/c` should yield `{"path": "a/b/c"}`.

`*` only makes sense at the end of a template: it means "from here to the end of the request." On `*`, join `request[index:]` and return; do not require equal length.

`/users/:id` against `/users/42` should beat `/users/*rest`: a param is more specific than a wildcard.

## What the lab asks for

On top of chapter 2:

- `/users/new` (static) beats `/users/:id`
- `/users/:id` beats `/users/*rest`
- `/files/*path` captures multiple segments
- Old static / param / method-mismatch behavior stays the same
