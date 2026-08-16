# 源码导读：路径参数

## 核心文件：`mini_router/router.py:11-13` 与 `:57-64`、`:110-125`

### 为什么先切段（:11-:13）

`split_path` 是参数匹配的前提。整串 `/users/:id` 无法和 `/users/42` 比较；切成段之后，比较的单位变成「这一格是字面量还是规则」。

### 注册时分流（:57-:64）

```
if any(seg.startswith(":") or seg.startswith("*") for seg in segments):
    self._dynamic.append((method, segments, handler))
    return
self._static[(method, path)] = handler
```

动态表存的是已经切开的 `segments`，查找时不必反复 split 模板。`:` 和 `*` 用前缀识别，而不是正则——规则的语法是路由器自己定义的，不必把路径交给 regex 引擎。

### `_match`：规则解释器（:110-:125）

逐段：

1. `*` 开头：剩余请求段全部吃掉（下章才用，本章实现可以先忽略）
2. 请求段不够了：失败
3. `:` 开头：写入 `params[name] = request[index]`
4. 否则必须字面相等
5. 走完模板后，请求段也必须刚好用完

最后一步很关键。少了它，`/users/:id` 会误吃 `/users/42/extra`。

本章你要亲手写出 3、4、5。不要对 `:id` 做 `==`。
