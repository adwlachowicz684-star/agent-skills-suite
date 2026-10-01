---
name: skill-aggregation
description: 多路结果合成一份时的失败——扇出并行的 N 个半成品（每个都对、合起来错、0 报错）、覆盖率的分母必须由编排层给出、partial 必须传递而不得被加工成完整报告、多路结果互相矛盾时模型默认取一个而不报冲突、顺序敏感性测试判定能否并行。用于「并行跑完每个都对但合起来不对」「汇总比预期少但不报错」「两个来源给出不同数字，输出里却只有一个」「不知道能不能并行」。不用于链级定位（见 skill-chain-failure）、单个技能内部的输出契约（见 skill-output）、调哪个技能的路由（见 skill-orchestration）。
license: MIT
---
# 汇总：多路结果合成一份时，什么会悄悄错

> 前置：《skill-composition》（该不该串、串成什么形状）·《skill-execution》（单个技能怎么跑）·
> 《skill-interfaces》（技能间传什么）
> 分工：《skill-composition》定 ⭐⭐⭐⭐ **串成什么形状**；
> 《skill-chain-failure》定 ⭐⭐⭐⭐⭐ **链坏了怎么定位**（出错地≠报错地、错误被逐级改写、重试放大、环路）；
> 本技能定 ⭐⭐⭐⭐⭐ **多路结果合成一份时的失败**——
> 它既发生在链里，也发生在**单个技能内部合并多来源**时。
> 目录：[1 扇出扇入](#1--扇出扇入n-个半成品) · [2 覆盖率](#2--覆盖率与-partial-传递) ·
> [3 矛盾](#3--多路结果互相矛盾) · [4 能否并行](#4--顺序敏感性测试) · [5 速查](#5-速查)

---

## 1. ⭐⭐⭐⭐⭐ 扇出扇入：N 个半成品

| | 串行 | ⭐ 并行 |
|---|---|---|
| 失败时状态 | 卡在某步 | ⭐⭐⭐⭐⭐ N 个半成品 |
| 报错 | 一个 | ⭐⭐⭐⭐⭐ 可能 0 个 |

> ⭐⭐⭐⭐⭐ **N 个半成品：每个单独看都是成功的，合起来是错的，没有任何组件会报错。**

三条硬规则：

```
① ⭐⭐⭐⭐⭐ 汇总必须报覆盖率（"3 个来源中 2 个成功，覆盖率 67%"）
② ⭐⭐⭐⭐⭐ 部分成功必须传 partial，下游不得按全量处理
③ ⭐⭐⭐⭐ 顺序敏感性测试：A→B 与 B→A 结果不同 → 禁止并行
```

第③条的价值：**不需要你事先知道依赖在哪**——它把"证明无依赖"变成了两次运行。
详见 `skill-aggregation/references/fan-out-fan-in.md`。

---

## 2. ⭐⭐⭐⭐⭐ 覆盖率与 partial 传递

> ⭐⭐⭐⭐⭐ **汇总把"部分成功"加工成了"完整报告"——而这一步没有任何组件报错。**

核心是分母：⭐⭐⭐⭐⭐ **覆盖率的分母必须由编排层给出**——
若由"成功返回的那几路"自己报，覆盖率永远接近 100%。

> ⭐⭐⭐⭐⭐ 编排器是链条上唯一"知道全局"的组件，所以覆盖率、partial 传递只能由它负责——
> 单个技能报的"成功"是⭐ **对自己而言的成功**。

详见 `skill-aggregation/references/partial-aggregation.md`。

---

## 3. ⭐⭐⭐⭐⭐ 多路结果互相矛盾

```
来源 A：新增用户 1,204
来源 B：新增用户 1,187
输出：  新增用户 1,187
```

> ⭐⭐⭐⭐⭐ 两个数字都进了上下文，输出里只剩一个——
> 而"选了一个"这件事没有任何地方写着。

这是"多个合法候选时选哪个"的汇总版本，但更危险：⭐⭐⭐⭐⭐ **矛盾本身就是最有价值的信息**
（说明两个来源口径不同），而汇总的默认动作是**把矛盾消掉**。

三条规则：

```
① ⭐⭐⭐⭐⭐ 差值超阈值 → 报冲突，不得静默取一个
② ⭐⭐⭐⭐⭐ 取一个时必须标注来源与口径（"按 A 口径"）
③ ⭐⭐⭐⭐ 口径不同 → 并列呈现，不做平均
```

第③条最常被违反：**平均是最像"解决了冲突"的动作**，而它产生一个两个来源都不支持的数字。

详见 `skill-aggregation/references/merge-conflict-resolution.md`。

---

## 4. 顺序敏感性测试

```
按 A→B 跑一次，记 R1；按 B→A 跑一次，记 R2
⭐⭐⭐⭐⭐ R1 ≠ R2 → 禁止并行
```

它不需要事先知道依赖在哪，两次运行就能判定——**这是唯一一种零先验的并行安全性测试**。

---

## 5. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ 并行跑完，每个都对、合起来不对 | `skill-aggregation/references/fan-out-fan-in.md` |
| ⭐⭐⭐⭐⭐ 汇总结果比预期少但不报错 | `skill-aggregation/references/partial-aggregation.md` |
| ⭐⭐⭐⭐⭐ 两个来源数字不同，输出里只有一个 | `skill-aggregation/references/merge-conflict-resolution.md` |
| ⭐⭐⭐⭐ 并行失败了要不要重跑单个分支 | 《skill-recovery》的 `skill-recovery/references/idempotency-resume.md` |
| ⭐⭐⭐⭐ 层数多、每层重试导致调用数失控 | `skill-chain-failure/references/retry-amplification.md` |

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-aggregation/references/fan-out-fan-in.md` | ⭐⭐⭐⭐⭐ 扇出并行、N 个半成品、顺序敏感性、汇总契约 |
| `skill-aggregation/references/partial-aggregation.md` | ⭐⭐⭐⭐⭐ 覆盖率分母、缺失偏差、partial 不得被加工成全量 |
| `skill-aggregation/references/merge-conflict-resolution.md` | ⭐⭐⭐⭐⭐ 多路结果矛盾：报冲突 / 标注口径 / 不做平均 |
