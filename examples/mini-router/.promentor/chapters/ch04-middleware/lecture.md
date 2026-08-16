# 中间件洋葱模型

这个 Chapter 学的是：把日志、鉴权、改 header 这类横切逻辑从每个 handler 里抽出来，包成一层层 `next`。

它在系统中的位置：`find_route` 已经找到人了。`handle` 负责造出 `Request`、套上中间件、调用 handler、保证未匹配时返回 404。

## 不要在每个 handler 里复制

```python
def show_user(request):
    log(request)
    user = load(request.params["id"])
    log_done()
    return Response(200, user)
```

三个 handler 就要写三遍。漏一次就出现「有的接口没日志」。横切关注点不属于业务函数。

中间件的形状：

```python
def logger(request, nxt):
    response = nxt(request)
    response.headers["X-Path"] = request.path
    return response
```

它拿到 `next`，决定何时调用、是否短路（鉴权失败可以直接 `return Response(401)`）。

## 洋葱：注册正向，包裹反向

`use(A); use(B)` 之后，一次请求的调用是：

```text
A 进入 → B 进入 → handler → B 离开 → A 离开
```

实现手法：从 handler 往外卷。先让 `wrapped = handler`，再 `for mw in reversed(middleware): wrapped = lambda req: mw(req, wrapped)`。

正序 for 会得到 B 在最外层，日志和鉴权的顺序就反了。闭包必须把当前的 `mw` 和 `nxt` 绑进默认参数，否则循环变量会全部指向最后一次。

## handle 是唯一入口

`find_route` 只回答「谁、什么参数」。`handle` 才执行：

1. 查找
2. 把 params 写进 `request.params`
3. 没有 handler → `Response(404, "not found")`，不要抛
4. handler 若返回普通值，包成 `Response(200, str(value))`
5. 套上中间件再调用

404 也是一种响应。调用方（下一章的 HTTP 适配）只认 `Response`。

## Lab 要实现什么

`Request` / `Response` 已经写在脚手架里，不要改字段名。

你要实现：

- `use(middleware)`：按调用顺序登记
- `handle(request)`：查找 + 洋葱 + 404

查找继续用你自己的 `find_route`。测试会检查中间件顺序、params 是否进了 request、未匹配是否 404。
