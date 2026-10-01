---
name: skill-interfaces
description: 技能之间传什么、怎么传——交接包契约、交接粒度、契约演进与消费声明、值与单位随行。用于「A 的输出要给 B 用」「中间产物怎么定」「跨技能边界时信息为什么会丢」「改了个字段下游为什么悄悄错了」。不用于单技能内部流程（见 skill-execution）、调哪个技能的路由（见 skill-orchestration）、组合的形态（见 skill-composition）。
license: MIT
---
# 技能间接口
> 前置：《skill-execution》（单个技能怎么跑）·《skill-output》（输出契约）·
> 《skill-composition》（组合形态）
> 分工：《skill-composition》定⭐ **谁和谁组合**；本技能定⭐⭐⭐⭐⭐ **它们之间传什么**；
> 《skill-execution》定⭐⭐⭐ **单个技能内部怎么产生这些东西**。
> 目录：[1 交接不是"把输出给下一个"](#1--交接不是把输出给下一个) · [2 交接包必须有 failures](#2--交接包里必须有-failures) ·
> [3 文件是 API](#3--文件是-api不是便签) · [4 不确定性递减](#4--不确定性在传递中递减) ·
> [5 上下文是涂改的黑板](#5--上下文是所有人都在涂改的黑板) · [6 Critical Rules](#6--critical-rules) · [7 何时不用](#7-何时不用) · [8 速查](#8-速查)

---

## 1. ⭐⭐⭐⭐⭐ 交接不是"把输出给下一个"

最常见的定义"上游输出即下游输入"只覆盖了值，漏掉三样：**状态 · 分母 · 来源**（+ 原因）。

> ⭐⭐⭐⭐⭐ 少了任何一样，下游都会**自己补一个**——而补的一定是看起来最正常的（ok / 100%），不是正确的。
> ⭐⭐⭐⭐⭐ 验证法：**删掉 status 跑一次，下游毫无察觉 = 这个字段从来没被读过。**
> 详见 `skill-interfaces/references/what-a-handoff-carries.md`。

---

## 2. ⭐⭐⭐⭐⭐ 交接包里必须有 failures

> ⭐⭐⭐⭐⭐ "分析完成，12,480 行"技术上完全真实、⭐⭐⭐⭐⭐ 而且完全误导——
> 它省略了 `source_b 401 → 覆盖率 67%`。⭐⭐⭐⭐⭐ **没有一方在撒谎，是协议里没有这个字段。**

五项必填：`status · coverage · failures · artifacts · ⭐⭐⭐⭐⭐ basis`
详见 `skill-interfaces/references/handoff-payload-contract.md`。

---

## 3. ⭐⭐⭐⭐⭐ 文件是 API，不是便签

中间产物必须有：`schema · version · status · ⭐⭐⭐⭐⭐ partial 标记`。

> ⭐⭐⭐⭐⭐ 最容易被漏的是 partial——下游把它当 ok，这是链式静默的主要来源。
> ⭐⭐⭐⭐⭐ "文件存在"过不了三种情况：**空 / 旧 / partial**——三种都不报错。
> ⭐⭐⭐⭐⭐ 自检："把这个文件给没参与这次运行的人，它能用吗？" 不能 → 它是便签。
> 详见 `skill-interfaces/references/artifact-as-api.md`。

---

## 4. ⭐⭐⭐⭐⭐ 不确定性在传递中递减

```
A: {"count": null, "status": "partial"}  →  B: {"count": 0, "status": "ok"}
```

> ⭐⭐⭐⭐⭐ **链条越长，末端越确定，也越可能错。**
> ⭐⭐⭐⭐⭐ 判据：**下游能区分"没有数据"和"没拿到数据"吗？** 不能 → 契约不完整，无论字段多全。
> 见 `skill-interfaces/references/artifact-mutation-in-chain.md`。

---

## 5. ⭐⭐⭐⭐⭐ 上下文是所有人都在涂改的黑板

> 临时字段塞进全局上下文、技能互相读彼此的结果 → ⭐⭐⭐⭐⭐ **出错的地方 ≠ 你改动的地方**。

修法：显式传参 + 会话级状态由编排层统一管理。检验：**拿到新会话单独跑，还能跑吗？**
详见 `skill-interfaces/references/skill-data-passing.md`。

---

## 6. ⭐⭐⭐⭐⭐ Critical Rules

```
MUST NOT 把交接定义为"上游输出即下游输入" —— 必须带 status/coverage/failures
MUST NOT 让 null 在下游变成 0 —— null 必须可达，且带 status 说明原因
MUST NOT 让 partial 在下游变成 ok —— 下游模板必须有 partial 的位置
MUST NOT 用"文件存在"判断"上游做过" —— 那是旧数据，不报错
MUST NOT 传值不传单位/时区/基准 —— 数字一样、语义差 1000 倍且不报错
MUST NOT 把临时字段塞进全局上下文 —— 出错的地方 ≠ 改动的地方
MUST NOT 传摘要而不传 coverage/retrieval/dropped —— 下游无法验证，且不报错
MUST NOT 原地改字段的语义 —— 改语义必须改字段名（duration → duration_s）
```

---

## 7. 何时不用

```
Do NOT 用于：
❌ 单技能内部的中间产物命名 —— 《skill-execution》的 `skill-execution/references/intermediate-artifacts.md`
❌ 决定调用哪个技能 —— 《skill-orchestration》的路由
❌ 组合的形态（顺序链/扇出/分支）—— 《skill-composition》
❌ ⭐⭐⭐⭐⭐ 只有一个技能 —— 不需要接口，直接写输出契约（见《skill-output》）
```

---

## 8. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ "共 N 条"真实但误导 | `skill-aggregation/references/partial-aggregation.md` |
| ⭐⭐⭐⭐⭐ null 变成 0、partial 变成 ok | `skill-interfaces/references/artifact-mutation-in-chain.md` |
| ⭐⭐⭐⭐⭐ 交接包该有哪些字段 | `skill-interfaces/references/handoff-payload-contract.md` |
| ⭐⭐⭐⭐⭐ 交接内容太大挤爆上下文 / 摘要丢了东西 | `skill-interfaces/references/handoff-granularity.md` |
| ⭐⭐⭐⭐⭐ 改了个字段，下游几周后才错 | `skill-interfaces/references/contract-evolution.md` |
| ⭐⭐⭐⭐⭐ 交接包字段写了但下游没在用 | `skill-interfaces/references/what-a-handoff-carries.md`（删字段测试） |
| ⭐⭐⭐⭐⭐ 中间产物被当便签写 | `skill-interfaces/references/artifact-as-api.md` |
| ⭐⭐⭐⭐ 技能互相读临时字段 | `skill-interfaces/references/skill-data-passing.md` |
| ⭐⭐⭐⭐ 交接的时机与协议 | `skill-interfaces/references/handoff-protocol.md` |
| ⭐⭐⭐ 中间产物命名/版本 | 《skill-execution》的 `skill-execution/references/intermediate-artifacts.md` |

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-interfaces/references/handoff-payload-contract.md` | ⭐⭐⭐⭐⭐ 交接包五项；缺 failures 是技术上真实的误导 |
| `skill-interfaces/references/handoff-granularity.md` | ⭐⭐⭐⭐⭐ 传内容/引用/摘要；摘要必须带 coverage+retrieval+dropped |
| `skill-interfaces/references/contract-evolution.md` | ⭐⭐⭐⭐⭐ 改语义最静默；消费声明写在下游；先停写再停读 |
| `skill-interfaces/references/artifact-mutation-in-chain.md` | ⭐⭐⭐⭐⭐ 不确定性在传递中递减；null→0、partial→ok；单位/基准随值传 |
| `skill-interfaces/references/skill-data-passing.md` | ⭐⭐⭐⭐ 显式传参 vs 全局上下文；上下文是涂改的黑板 |
| `skill-interfaces/references/handoff-protocol.md` | ⭐⭐⭐⭐ 交接的时机与协议约定 |
| `skill-interfaces/references/what-a-handoff-carries.md` | ⭐⭐⭐⭐⭐ 交接携带状态/分母/来源/原因；⭐⭐⭐⭐⭐ 删字段测试验证下游是否在用 |
| `skill-interfaces/references/artifact-as-api.md` | ⭐⭐⭐⭐⭐ 中间产物四字段；"存在"过不了空/旧/partial；便签 vs API 的判据 |
