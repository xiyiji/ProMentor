# 源码导读：组装

## 核心文件：`mini_router/demo.py:9-30` 与 `mini_router/server.py:10-32`

### 应用是「注册」，不是「再实现路由」（demo.py:9-22）

`build_app` 只做三件事：new Router、add_route、use。handler 是 lambda，直接读 `req.params` / `req.body`。中间件在 handler 之后改 header，所以一定先 `nxt(request)`。

对照你要写的 `app.py`：结构应当一样。差别只是 import 来自本章的 `router` / `server`，而不是包内相对路径。

### dispatch 是薄封装（demo.py:25-26）

一行 `router.handle(Request(...))`。不要在这里重新解析路径。解析属于 Router。

### HTTP 适配器（server.py:10-32）

`Handler` 闭包住外层的 `router`。`_dispatch` 是所有动词的汇合点：

1. 读 body（没有 `Content-Length` 就当空）
2. `path.split("?", 1)[0]` 丢掉 query
3. `router.handle(Request(self.command, path, body=body))`
4. 状态码、header、body 写回

`log_message` 被空掉，避免示范课跑起来刷屏。这不是设计要点。

要点是：应用代码从不继承 `BaseHTTPRequestHandler`。继承留在适配器里。
