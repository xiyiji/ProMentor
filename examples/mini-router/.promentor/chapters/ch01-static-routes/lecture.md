# 静态路由与精确匹配

这个 Chapter 学的是 HTTP 路由器最底层的能力：把 `(方法, 路径)` 精确映射到一个处理函数。没有它，后面的参数、通配符、中间件都无处挂载。

它在系统中的位置：请求进来的第一件事，就是问路由器「谁来处理」。

## 路由表是一张映射，不是一串 if

最容易想到的写法是：

```python
if method == "GET" and path == "/users":
    return list_users
if method == "GET" and path == "/health":
    return health
```

路由一多，这段代码就变成一份无法维护的清单。真正的结构是数据，不是控制流：

```text
("GET", "/users")  → list_users
("GET", "/health") → health
```

查找变成字典取值。新增路由是往表里插一行，而不是再加一个 `if`。

## 为什么 key 必须带上 method

`GET /users` 和 `DELETE /users` 是两条完全不同的规则。只按 path 索引，就无法表达 REST 里「同一路径、不同动词」这件事。

所以 key 是 `(method, path)`，不是 `path`。

## 为什么先做规范化

浏览器和客户端会写出 `/users` 和 `/users/`。对路由器来说它们应该是同一条静态规则，否则你会维护两份表。

`mini-router` 的约定：

- method 一律大写
- 去掉尾斜杠；根路径保持 `/`

规范化发生在**注册和查找两侧**。只规范一边，另一边对不上。

## 为什么静态路由用 dict，而不是 list

静态路径没有模式，整串要么相等要么不等。dict 的平均查找是 O(1)。

后面两章会看到：一旦路径里出现 `:id`，整串相等就失效了。那时再引入第二张表。现在不要过早抽象——精确匹配用最便宜的结构。

## Lab 要实现什么

实现 `Router.add_route` 和 `Router.find_route`，只要求静态路径：

- 注册 `GET /users` 后，查找返回同一个 handler，params 为空 dict
- method 或 path 对不上，handler 为 `None`
- `/users/` 与 `/users` 视为同一条

不要在这一章解析 `:id`。先把精确匹配做对。
