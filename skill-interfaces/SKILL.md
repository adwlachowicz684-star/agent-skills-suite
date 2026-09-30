---
name: skill-interfaces
description: 技能之间传什么、怎么传——交接包契约、协议、数据传递、值与单位随行。用于「A 的输出要给 B 用」「中间产物怎么定」「跨技能边界时信息为什么会丢」。不用于单技能内部流程（见 skill-execution）、调哪个技能的路由（见 skill-orchestration）、组合的形态（见 skill-composition）。
license: MIT
---
# 技能间接口
> 前置：《skill-execution》（单个技能怎么跑）·《skill-output》（输出契约）·
> 《skill-chaining》（组合形态）
> 分工：
> 《skill-composition》定⭐ **谁和谁组合**；
> 本技能定⭐⭐⭐⭐⭐ **它们之间传什么**；
> 《skill-execution》定⭐⭐⭐ **单个技能内部怎么产生这些东西**。
---

## 目录

- [1. ⭐⭐⭐⭐⭐ 交接不是"把输出给下一个"](#1--交接不是把输出给下一个)
- [2. ⭐⭐⭐⭐⭐ 交接包里必须有 failures](#2--交接包里必须有-failures)
- [3. ⭐⭐⭐⭐⭐ 文件是 API，不是便签](#3--文件是-api不是便签)
- [4. ⭐⭐⭐⭐⭐ 不确定性在传递中递减](#4--不确定性在传递中递减)
- [5. ⭐⭐⭐⭐⭐ 上下文是所有人都在涂改的黑板](#5--上下文是所有人都在涂改的黑板)
- [6. 何时不用](#6-何时不用)
- [7. 速查](#7-速查)

---

## 1. ⭐⭐⭐⭐⭐ 交接不是"把输出给下一个"

最常见的交接定义是"上游的输出就是下游的输入"。这漏掉了三样东西：

```
① ⭐⭐⭐⭐⭐ 状态（这次是成功、部分成功、还是失败？）
② ⭐⭐⭐⭐⭐ 分母（应该是多少，而不只是实际有多少）
③ ⭐⭐⭐⭐⭐ 来源（这个值从哪来，能回溯吗？）
```

> ⭐⭐⭐⭐⭐ 少了任何一样，下游都会**自己补一个**——
> 而补的那个一定是看起来最正常的，不是正确的。

---

## 2. ⭐⭐⭐⭐⭐ 交接包里必须有 failures

```
"分析完成，12,480 行，留存中位数 41%"
```

> ⭐⭐⭐⭐⭐ 这句话技术上完全真实，⭐⭐⭐⭐⭐ 而且完全误导——
> 它省略了 `source_b 401 → 覆盖率 67%`。

> ⭐⭐⭐⭐⭐ **没有一方在撒谎——是交接协议里没有这个字段。**

五项必填（详见 `skill-interfaces/references/handoff-payload-contract.md`）：

```
status · coverage · failures · artifacts · ⭐⭐⭐⭐⭐ basis（依据）
```

---

## 3. ⭐⭐⭐⭐⭐ 文件是 API，不是便签

中间产物必须有：

```
schema（字段与类型）· version · status · ⭐⭐⭐⭐⭐ 部分成功标记
```

> ⭐⭐⭐⭐⭐ 最容易被漏的是"部分成功"：
> ⭐⭐⭐⭐ `status: partial` 下游才知道要谨慎；
> ⭐⭐⭐⭐⭐ 否则下游把它当 ok，这是链式静默的主要来源。

---

## 4. ⭐⭐⭐⭐⭐ 不确定性在传递中递减

```
A: {"count": null, "status": "partial"}
B: {"count": 0,   "status": "ok"}
```

> ⭐⭐⭐⭐⭐ 链条越长，末端越确定，也越可能错。
> 改写的三种形态与三条修法见 `skill-interfaces/references/artifact-mutation-in-chain.md`。

关键判据：

> ⭐⭐⭐⭐⭐ **下游能不能区分"没有数据"和"没拿到数据"？**
> 不能 → 契约不完整，无论字段多全。

---

## 5. ⭐⭐⭐⭐⭐ 上下文是所有人都在涂改的黑板

```
早期我把临时字段塞进全局上下文、技能互相读彼此的结果
→ ⭐⭐⭐⭐⭐ 出错的地方 ≠ 你改动的地方
```

修法：显式传参 + 会话级状态由编排层统一管理。检验标准一句话：

> ⭐⭐⭐⭐⭐ **拿到新会话单独跑，还能跑吗？**

---

## 6. ⭐⭐⭐⭐⭐ Critical Rules

```
MUST NOT 把交接定义为"上游输出即下游输入" —— 必须带 status/coverage/failures
MUST NOT 让 null 在下游变成 0 —— null 必须可达，且带 status 说明原因
MUST NOT 让 partial 在下游变成 ok —— 下游模板必须有 partial 的位置
MUST NOT 用"文件存在"判断"上游做过" —— 那是旧数据，不报错
MUST NOT 传值不传单位/时区/基准 —— 数字一样、语义差 1000 倍且不报错
MUST NOT 把临时字段塞进全局上下文 —— 出错的地方 ≠ 改动的地方
```

---

## 7. 何时不用

```
Do NOT 用于：
❌ 单技能内部的中间产物命名 —— 那是《skill-execution》的 `skill-execution/references/intermediate-artifacts.md`
❌ 决定调用哪个技能 —— 那是《skill-orchestration》的路由
❌ 组合的形态（顺序链/扇出/分支）—— 那是《skill-chaining》
❌ ⭐⭐⭐⭐⭐ 只有一个技能 —— 不需要接口，直接写输出契约（见《skill-output》）
```

---

## 8. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ "共 N 条"真实但误导 | 《skill-chaining》的 `skill-chaining/references/partial-aggregation.md` |
| ⭐⭐⭐⭐⭐ null 变成 0、partial 变成 ok | `skill-interfaces/references/artifact-mutation-in-chain.md` |
| ⭐⭐⭐⭐⭐ 交接包该有哪些字段 | `skill-interfaces/references/handoff-payload-contract.md` |
| ⭐⭐⭐⭐ 技能互相读临时字段 | `skill-interfaces/references/skill-data-passing.md` |
| ⭐⭐⭐⭐ 交接的时机与协议 | `skill-interfaces/references/handoff-protocol.md` |
| ⭐⭐⭐ 中间产物命名/版本 | 《skill-execution》的 `skill-execution/references/intermediate-artifacts.md` |

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-interfaces/references/handoff-payload-contract.md` | ⭐⭐⭐⭐⭐ 交接包五项；缺 failures 是技术上真实的误导 |
| `skill-interfaces/references/artifact-mutation-in-chain.md` | ⭐⭐⭐⭐⭐ 不确定性在传递中递减；null→0、partial→ok；单位/基准随值传 |
| `skill-interfaces/references/skill-data-passing.md` | ⭐⭐⭐⭐ 显式传参 vs 全局上下文；上下文是涂改的黑板 |
| `skill-interfaces/references/handoff-protocol.md` | ⭐⭐⭐⭐ 交接的时机与协议约定 |
