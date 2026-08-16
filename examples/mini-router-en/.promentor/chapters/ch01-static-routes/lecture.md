# Static routes and exact matching

This chapter is the bottom layer of an HTTP router: map `(method, path)` onto a handler. Without that, params, wildcards, and middleware have nowhere to hang.

Where it sits in the system: the first question a request asks the router is "who handles this?"

## A routing table is a map, not a chain of ifs

The first draft everyone writes looks like this:

```python
if method == "GET" and path == "/users":
    return list_users
if method == "GET" and path == "/health":
    return health
```

Add enough routes and this becomes an unmaintainable checklist. The real structure is data, not control flow:

```text
("GET", "/users")  → list_users
("GET", "/health") → health
```

Lookup is a dict get. Adding a route is inserting a row, not another `if`.

## Why the key must include the method

`GET /users` and `DELETE /users` are two different rules. Index by path alone and you cannot express REST's "same path, different verb."

So the key is `(method, path)`, not `path`.

## Why normalize first

Browsers and clients write both `/users` and `/users/`. To the router those should be the same static rule, or you maintain two tables.

`mini-router` conventions:

- methods are always uppercased
- strip the trailing slash; the root stays `/`

Normalize on **both register and lookup**. Normalize only one side and the other will miss.

## Why a dict for static routes, not a list

A static path has no pattern: the whole string matches or it does not. Average dict lookup is O(1).

The next two chapters show that once `:id` appears, whole-string equality dies. That is when a second table appears. Do not abstract early — exact matching should use the cheapest structure.

## What the lab asks for

Implement `Router.add_route` and `Router.find_route` for static paths only:

- After registering `GET /users`, lookup returns that same handler and an empty params dict
- Wrong method or path → handler is `None`
- `/users/` and `/users` are the same route

Do not parse `:id` in this chapter. Get exact matching right first.
