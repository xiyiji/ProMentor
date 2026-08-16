# Path parameters: a rule is not a literal

This chapter: a `:id` segment is not a string, it is a capture rule. The static table's `==` dies here.

Where it sits: after a static miss, the router must interpret the request path as a pattern and hand captured params to the handler.

## Why whole-string comparison is not enough

You can already match `/users`. Now you need `/users/42` and `/users/7`, and the handler must see `{"id": "42"}`.

If you keep using a dict key:

```text
("GET", "/users/42") → show_user
```

every user id has to be registered first. A routing table describes **rules**, not URLs you have already seen.

## Segments, not the whole path

Split the path:

```text
pattern:  /users/:id   →  ["users", ":id"]
request:  /users/42    →  ["users", "42"]
```

Walk them pair-wise:

- `users` vs `users`: literal match, continue
- `:id` vs `42`: this is a rule. Do not `==`. Store `id=42` in params

Wrong segment count (`/users/42/extra`) is a miss. Nested is the same idea: `/users/:uid/posts/:pid` against `[users, 1, posts, 9]`.

## Keep the two tables

Once `:id` appears, people fold every route into a linear scan. Don't.

- No `:` / `*` → stay in the static dict
- Has a pattern → dynamic table, store the **segment list**, not the raw string

Lookup order: static first, then dynamic. An exact path like `/users` should not get slower just because params exist.

## The usual bug

`==` between `:id` and `42`. Tests will show empty `params` — the compare never succeeded, or it succeeded and you never captured.

`:id` means: accept **any** value in this slot, and remember it.

## What the lab asks for

`add_route` / `find_route` must support both:

- static paths (chapter 1 behavior still required)
- `/users/:id` → params `{"id": "42"}`
- `/users/:uid/posts/:pid` → two params
- wrong length or method → `(None, {})`

Skip `*path` and priority. That is the next chapter.
