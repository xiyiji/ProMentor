# 组装可运行的 Mini Router

这个 Chapter 把前四章的路由器拼成一个能跑的小 API。学完你应该能 `python3 .promentor/main.py` 起一个服务，而不是只剩一堆单元测试。

它在系统中的位置：Router 是内核，这一章是外壳——注册真实路由、接上 HTTP。

## 内核已经有了，不要再造一套

`router.py` 和 `server.py` 是课程提供的完整实现（相当于你做完前四章之后的结果）。**不要改它们。** 作业只有 `app.py`：决定有哪些 URL、中间件做什么、如何把一次调用变成 `Response`。

这和真实框架一样：你很少重写路由器，你在写应用。

## build_app：路由表就是产品

最小集合：

| 方法 | 路径 | 行为 |
|------|------|------|
| GET | `/` | body 为 `mini-router` |
| GET | `/users/:id` | body 为 id |
| GET | `/files/*path` | body 为剩余路径 |
| POST | `/echo` | body 原样返回 |

再挂一个 logger：调用 `next` 之后，给响应加上 `X-Path` header（值为请求 path）。这是在验证你真的把中间件接到了应用上，而不是只在测试里 extra 调 `use`。

## dispatch：给测试和给 HTTP 同一条路

```python
def dispatch(router, method, path, body=""):
    return router.handle(Request(method, path, body=body))
```

测试走 `dispatch`，不绑端口。`run` 再把同一个 `router` 交给 `server.run`。两条入口，一个内核——否则你会为「单测能过、浏览器 404」debug 一整晚。

## server.py 在做什么（读，不用写）

stdlib 的 `BaseHTTPRequestHandler` 按动词拆成 `do_GET` / `do_POST`。适配器把它们收拢成一次 `router.handle(Request(...))`，再把 `Response` 写回。查询串丢掉，body 按 `Content-Length` 读。

路由器不知道 HTTP。HTTP 不知道路由表。这是边界。

## Lab 要实现什么

在 `app.py` 里实现 `build_app`、`dispatch`、`run`。签名见 `lab.json`。

写完后：

```bash
python3 .promentor/chapters/ch05-assemble/lab_test.py
python3 .promentor/main.py
```

浏览器打开 `http://127.0.0.1:8000/` 应看到 `mini-router`。
