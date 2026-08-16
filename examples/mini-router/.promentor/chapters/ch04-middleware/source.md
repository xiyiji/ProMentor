# 源码导读：中间件

## 核心文件：`mini_router/router.py:23-46` 与 `:88-107`

### Request / Response 是适配层的协议（:23-:46）

它们很瘦：method、path、params、body；status、body、headers。路由器不依赖 `http.server`。后面 `server.py` 只负责把 stdlib 的请求填进 `Request`，再把 `Response` 写回 socket。

把协议留在自己的类型里，测试才能不绑端口。

### `use` 只登记（:88-:89）

中间件列表是有序的。`use` 不做包裹——包裹发生在每次 `handle`，这样后注册的中间件对已经存在的路由立刻生效。

### `handle` 由内向外卷（:91-:107）

```
def leaf(req):
    result = handler(req)
    return result if isinstance(result, Response) else Response(200, str(result))

wrapped = leaf
for middleware in reversed(self._middleware):
    nxt = wrapped
    wrapped = lambda req, _mw=middleware, _nxt=nxt: _mw(req, _nxt)
return wrapped(request)
```

三处值得停一下：

1. `reversed`：先注册的成为最外层。
2. `_mw=middleware, _nxt=nxt`：绑定当次循环的值。写成 `lambda req: middleware(req, wrapped)` 会让所有层指向最后一次赋值。
3. 404 在卷洋葱之前返回。未匹配的请求不跑中间件——这是本课约定，测试按此断言。
