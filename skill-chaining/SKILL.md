---
name: skill-chaining
description: 该不该把多个技能串成链，以及链了之后失败会长成什么样——升级阈值、过早编排、链式失败三种形状、覆盖率与 partial 传递。用于「这个任务要不要用几个技能协作」「链跑出来的结果不对但不知道哪一级错了」。不用于组合的具体写法（见 skill-composition）、技能间接口契约（见 skill-interfaces）、触发哪个技能的路由决策（见 skill-orchestration）。
license: MIT
---

# 技能链：该不该串，串了会怎么坏

> 前置：《skill-authoring》（单技能怎么写）·《skill-execution》（单个技能怎么跑）·
> 《skill-interfaces》（技能间接口契约）
> 分工：
> 《skill-orchestration》决定⭐ **调哪个**；
> 《skill-composition》决定⭐⭐⭐⭐ **它们按什么形状组合**；
> 本技能决定⭐⭐⭐⭐⭐ **该不该串，以及串了之后失败长什么样**。

---

## 目录

- [1. ⭐⭐⭐⭐⭐ 先问：真的需要链吗](#1--真的需要链吗)
- [2. ⭐⭐⭐⭐⭐ 链式失败的形状](#2--链式失败的形状)
- [3. 何时不用](#3-何时不用)
- [4. 速查](#4-速查)

---

## 1. ⭐⭐⭐⭐⭐ 先问：真的需要链吗

```
提示词复制 2 次以上   → 升为技能
⭐⭐⭐⭐⭐ 技能输出手动搬运 3 次以上 → 升为编排器
```

> ⭐⭐⭐⭐⭐ 两处数字不同不是矛盾——**层级越高、升级成本越大，所以要求的证据越多**。

过早编排是新的过早抽象：

```
❌ 不要从这里起步
✅ 先做第一个技能 → 第二个
⭐⭐⭐⭐⭐ 当你发现自己把其中一个的输出复制粘贴到另一个里超过三次
   → 那时才写编排器
```

判据（与 `skill-scoping/references/no-op-and-value.md` 同构）：

> ⭐⭐⭐⭐⭐ **如果模型不编排也会自己串起来，这个编排器没有价值。**

---

## 2. ⭐⭐⭐⭐⭐ 链式失败的形状

单技能失败时，你知道是哪个技能。链式失败时：

```
A → B → C 中 B 出错
⭐⭐⭐⭐⭐ C 的失败报告里根本不会提到 B
```

> ⭐⭐⭐⭐⭐ **出错的地方 ≠ 报错的地方。**
> 这是链式结构最贵的属性，也是它必须配可观测性的原因。

三个必然出现的失败类型：

| 类型 | 表现 | ⭐ 关键点 |
|---|---|---|
| ⭐⭐⭐⭐⭐ 中间产物缺失 | 下游拿到空/旧文件 | 用"文件存在"判断"做过"是错的 |
| ⭐⭐⭐⭐⭐ 部分成功被当全成功 | 上游 2/3 成功，下游按全量处理 | `status: partial` 必须传递 |
| ⭐⭐⭐⭐⭐ 错误被逐级改写 | A 返回错误，B 当输入，C 输出"成功" | 每级都要显式检查上游状态 |

> ⭐⭐⭐⭐⭐ 第三种最危险：⭐⭐⭐⭐ **每一级都在正常完成自己的工作**，
> ⭐⭐⭐⭐⭐ 合起来把一个错误加工成了一份看起来成功的报告。

⭐⭐⭐⭐⭐ 唯一的结构性对策是**每级显式检查上游状态**——
不能靠"下游自然会发现问题"，因为下游拿到的仍然是格式正确的输入。

---

## 3. 何时不用

```
Do NOT 用于：
❌ 单技能内部的步骤顺序 —— 那是《skill-execution》的 `skill-execution/references/sequential-dependency.md`
❌ 技能之间传什么字段 —— 那是《skill-interfaces》的 `skill-interfaces/references/handoff-payload-contract.md`
❌ 决定触发哪一个技能 —— 那是《skill-orchestration》的路由
❌ 组合形态、编排器写法、扇出扇入规则 —— 那是《skill-composition》
❌ ⭐⭐⭐⭐⭐ 顺序必须强制且只有一两个技能 —— 改用脚本或工作流
❌ 任务本身不稳定、每次流程都不同 —— 那是"对话"，不是链
```

> ⭐⭐⭐⭐⭐ 最后一条最容易误判：⭐⭐⭐⭐ 流程每次都变说明还没沉淀出模式，
> ⭐⭐⭐⭐⭐ 此时写编排器会把"还没成形的东西"固化成结构。

---

## 4. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ 报错的技能不是真正出错的技能 | `skill-orchestration/references/composition-patterns-types.md`（隐式依赖） |
| ⭐⭐⭐⭐⭐ 汇总结果比预期少但不报错 | `skill-chaining/references/partial-aggregation.md` |
| ⭐⭐⭐⭐⭐ 报错的技能不是出错的技能、不知断在哪一级 | `skill-chaining/references/chain-failure-localization.md` |
| ⭐⭐⭐⭐⭐ 该不该写编排器 | `skill-orchestration/references/orchestrator-timing.md` |
| ⭐⭐⭐⭐ 技能互相读对方的临时字段 | `skill-interfaces/references/skill-data-passing.md` |
| ⭐⭐⭐⭐ 两个技能都要改同一份文件 | `skill-orchestration/references/collision-arbitration.md` |
| ⭐⭐⭐ 组合后注入面变大 | `skill-orchestration/references/prompt-injection.md` |

> ⭐⭐⭐⭐⭐ 汇总那条的三个要点：
> ⭐⭐⭐⭐⭐ "共 200 条"真实且误导；⭐⭐⭐⭐⭐ 缺失不是随机的会扭曲趋势；
> ⭐⭐⭐⭐⭐ 分母必须来自扇出清单，不能来自"成功返回的条数"。

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-chaining/references/partial-aggregation.md` | ⭐⭐⭐⭐⭐ 汇总的覆盖率、缺失偏差、分母来源 |
| `skill-chaining/references/chain-failure-localization.md` | ⭐⭐⭐⭐⭐ 链路 ID、从后往前二分定位、每级检查上游状态 |
| `skill-orchestration/references/composition-patterns-types.md` | ⭐⭐⭐⭐⭐ 四种依赖类型、三个反模式、隐式依赖 |
| `skill-orchestration/references/orchestrator-timing.md` | ⭐⭐⭐⭐⭐ 过早编排=过早抽象；手动搬运>3次才写 |
| `skill-composition/references/fan-out-fan-in.md` | ⭐⭐⭐⭐⭐ 扇出并行、汇总、覆盖率 |
| `skill-composition/references/protocol-layering.md` | ⭐⭐⭐⭐ MCP 与技能的分层原则 |
