# Helper 库模式：给函数，不给流程

> 相关：`skill-scripting/references/tool-output-design.md`（输出是模型的原材料）·
> `skill-scripting/references/script-cli-contract.md`（退出码分级）· `skill-scripting/references/deterministic-scripts.md`（纯函数）
> 前置：那些讲⭐ 单个脚本怎么写，
> 这份讲⭐⭐⭐⭐ **一族脚本怎么组织**——以及为什么这比写流程更有效。

---

## 目录

- [1. ⭐⭐⭐⭐⭐ 两种给法](#1--两种给法)
- [2. ⭐⭐⭐⭐⭐ docstring 是 Gotchas 的第二投放点](#2--docstring-是-gotchas-的第二投放点)
- [3. ⭐⭐⭐ 库 vs 端到端脚本：什么时候用哪种](#3--库-vs-端到端脚本什么时候用哪种)
- [4. ⭐⭐⭐⭐ 函数设计的四条](#4--函数设计的四条)
- [5. ⭐⭐⭐ 让模型现场组合](#5--让模型现场组合)
- [6. ⭐⭐ 反模式](#6--反模式)

---

## 1. ⭐⭐⭐⭐⭐ 两种给法

```
A) 端到端脚本：skill 调一次，出结果
B) ⭐ helper 库：给一组函数，模型现场拼出它这次需要的脚本
```

多数人只想到 A。但官方给的判断是：

> ⭐⭐ **你能给 Claude 的最强工具之一就是代码。**
> 有了脚本和库，Claude 就能把回合花在**组合**上——决定下一步做什么，
> 而不是每次重建样板代码。

```
场景："周二发生了什么？"

A) 你得预先写好 weekly_report.py ——但它回答不了
   "周二下午三点之后、只算移动端"这种没预料的问法

B) ⭐ 给 fetch_events(start, end, filters) + 几个聚合函数
   模型现场写 12 行脚本，精确回答这个问法
```

> ⭐⭐⭐ **A 的问题是"你预想到了才算"，B 的能力边界是模型的组合能力。**

---

## 2. ⭐⭐⭐⭐⭐ docstring 是 Gotchas 的第二投放点

> ⭐⭐ **把 gotchas 写进 docstring。**

为什么这比写在 references 里更可靠：

| 投放点 | 命中条件 |
|---|---|
| gotchas.md | ⭐ 模型恰好去读了那个文件 |
| ⭐ **函数 docstring** | ⭐⭐ 模型一旦要用这个函数，就在它眼前 |

```python
def fetch_events(start, end, filters=None):
    """Fetch raw events from the event source.

    GOTCHA: the events table is append-only. For a given event_id,
    take the row with the highest `version`, not the latest `created_at`.

    GOTCHA: `ts` is UTC. Do not compare against local time directly.
    """
```

> ⭐ **这是"把知识放到它会被用到的那一刻"（渐进式披露）在函数层的实现。**

---

## 3. ⭐⭐⭐ 库 vs 端到端脚本：什么时候用哪种

| 判据 | 选 |
|---|---|
| ⭐ 问法可枚举（每次就那几种） | 端到端脚本 |
| ⭐ 问法开放（"周二发生了什么"这类） | helper 库 |
| 失败代价高、必须一模一样 | ⭐ 端到端脚本 + 精确命令 |
| 需要多步串起来且中间要判断 | helper 库 |

> ⭐⭐ **两者不互斥**：常见的成熟形态是
> **一个端到端脚本负责高频主路径 + 一个 helper 库兜住开放问法。**

---

## 4. ⭐⭐⭐⭐ 函数设计的四条

**① 函数名即文档**

```
❌ get_data(x)
✅ fetch_events(start, end, filters)
```

模型是**照着名字决定用不用**的（与工具命名同理：`skill-scripting/references/tool-output-design.md`）。

**② 参数显式，不用全局状态**

```
❌ 依赖环境变量里的默认时间范围
✅ fetch_events(start, end)   —— 时间必须由调用方传入
```

⭐ 这与纯函数四原则一致（`skill-scripting/references/deterministic-scripts.md`）：
`datetime.now()` 藏在库内部 = 每次跑结果不同 = 不可测。

**③ 错误消息要能自纠**

```
❌ "Error: bad input"
✅ "Invalid ticker 'XYZ' — try a 4-letter ticker like 'AAPL'."
```

模型看到的是 stderr 的全部。**不告诉它下一步做什么，它就会重试九次**
（`skill-security/references/hooks-skill-cooperation.md` 里的实测）。

**④ 返回要小**

```
❌ 返回 10000 token 的原始 JSON
✅ 返回摘要 + 计数 + 指向完整结果的引用
```

⭐⭐ **返回值会进上下文，而库函数会被多次调用**——
一次胖返回，会在后续每一轮持续收费。

---

## 5. ⭐⭐⭐ 让模型现场组合

SKILL.md 里要**明确写出这个用法**，否则模型会以为只能直接调脚本：

```markdown
## 用 helper 库

`scripts/lib/` 提供取数与聚合函数。
⭐ 不要为每个新问题写新脚本——先查 lib 里有什么，
用它们现场组合出分析脚本，写到 /tmp 再执行。

各函数的 docstring 里写了已知的坑，用之前读一下。
```

三个细节：

1. ⭐ **指明"写到 /tmp 再执行"**——别让生成的代码污染仓库
2. ⭐ **指明"先查 lib 里有什么"**——否则它会重新造一遍
3. ⭐ **指明"读 docstring"**——否则 gotchas 白写

---

## 6. ⭐⭐ 反模式

| 反模式 | 后果 |
|---|---|
| ⭐ 库里塞了端到端逻辑 | 复用不了，退化成 A 却没有 CLI 契约 |
| 函数返回结果过大 | 每次调用都往上下文倒一堆，多轮后爆掉 |
| ⭐ docstring 只写"做什么" | gotchas 无处安放，模型重复踩坑 |
| 参数靠全局默认值 | 不可测、不可复现 |
| ⭐ 不写"现场组合"这几个字 | 模型每次现造样板代码，等于没给库 |

---

## 与已有判据的关系

`skill-scripting/references/deterministic-scripts.md` 给的判据是：

```
"从 Y 算出 X，X 是数字、Y 是结构化数据" → 脚本
"用自然语言解释 X"                      → LLM
```

本份补的是**中间那一档**：

```
⭐ "X 是什么取决于这次的问法" → helper 库 + 模型现场组合
```
