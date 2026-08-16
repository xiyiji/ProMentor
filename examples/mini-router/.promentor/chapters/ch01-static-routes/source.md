# 源码导读：静态路由

## 核心文件：`mini_router/router.py:11-71`

### 路径切分与规范化（:11-:20）

`split_path` 丢掉空段，所以 `/users/42/` 和 `/users/42` 得到同一组 segment。`normalize_path` 保证 key 稳定：缺前导 `/` 就补上，尾斜杠去掉，空路径变成 `/`。

这两步看起来像工具函数，其实是在定义路由表的相等性。相等性没定清楚，后面所有查找都是错的。

### 两张表，而不是一张（:49-:55）

```
_static  : (METHOD, /path) → handler     # 精确匹配
_dynamic : [(METHOD, segments, handler)] # 本章先不用
```

原始设计把「能 O(1) 的」和「必须走模式匹配的」从注册那一刻就分开。如果全塞进 list，静态路由也会变成线性扫描。

### 注册：有模式才进动态表（:57-:64）

`add_route` 先规范化，再看 segment 是否以 `:` 或 `*` 开头。本章你的实现可以更简单：只写入 `_static`。但要理解这个分叉——它决定了查找时为什么能先做一次 dict get。

### 查找：静态命中立刻返回（:66-:71）

```
static = self._static.get((method, path))
if static is not None:
    return static, {}
```

静态命中不走后面的循环。`/users/new` 如果同时存在 `/users/:id`，静态表先赢——这是第 3 章优先级的基础，根子在这里。
