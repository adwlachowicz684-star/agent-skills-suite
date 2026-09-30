---
name: skill-composition
description: 多个技能该不该串、串成什么形状——升级阈值、过早编排、顺序链/扇出扇入/条件分支/流水线、链式失败三种形状、覆盖率与 partial 传递、编排器该不该写、协议分层（MCP 是普通话，技能是方言）。用于「这个任务要不要用几个技能协作」「几个技能怎么搭」「要不要并行」「链跑出来的结果不对但不知道哪一级错了」。不用于技能间字段契约（见 skill-interfaces）、触发哪个技能的路由决策（见 skill-orchestration）、单个技能内部怎么跑（见 skill-execution）。
license: MIT
---
# 技能组合：该不该串，串成什么形状，串了会怎么坏

> 前置：《skill-authoring》（单技能怎么写）·《skill-execution》（单个技能怎么跑）·
> 《skill-interfaces》（技能间传什么）
> 分工：《skill-orchestration》定⭐ **调哪个**；本技能定⭐⭐⭐⭐⭐ **该不该串、串成什么形状、串了怎么坏**；
> 《skill-interfaces》定⭐⭐⭐⭐ **它们之间传什么**。
> 目录：[1 先问真的需要链吗](#1--先问真的需要链吗) · [2 四种形态](#2-组合的四种形态) ·
> [3 编排器写不写](#3--编排器写还是不写) · [4 扇出扇入](#4--扇出与扇入) ·
> [5 链式失败](#5--链式失败的形状) · [6 协议分层](#6--协议分层) · [7 何时不用](#7-何时不用) · [8 速查](#8-速查)

---

## 1. ⭐⭐⭐⭐⭐ 先问：真的需要链吗

```
提示词复制 2 次以上              → 升为技能
⭐⭐⭐⭐⭐ 技能输出手动搬运 3 次以上 → 升为编排器
```

> ⭐⭐⭐⭐⭐ 两处数字不同不是矛盾——**层级越高、升级成本越大，所以要求的证据越多**。
> 过早编排是新的过早抽象：❌ 不要从这里起步；✅ 先做第一个技能 → 第二个，
> ⭐⭐⭐⭐⭐ 把其中一个的输出复制粘贴到另一个里超过三次，那时才写编排器。
> 判据：**如果模型不编排也会自己串起来，这个编排器没有价值**——与 `orchestrator-timing.md` 同源。

---

## 2. 组合的四种形态

| 形态 | 结构 | ⭐ 失败点 |
|---|---|---|
| 顺序链 | A → B → C | ⭐⭐⭐⭐ 中间产物 |
| ⭐⭐⭐⭐⭐ 扇出扇入 | A → {B,C,D} → 汇总 | ⭐⭐⭐⭐⭐ 部分成功 |
| ⭐⭐⭐⭐ 条件分支 | 按输入选一条 | ⭐⭐⭐⭐ 分支未覆盖输入 |
| ⭐⭐⭐ 流水线 | 每级产出一个产物 | ⭐⭐⭐⭐⭐ 错误被逐级改写 |

依赖类型与三个反模式见 `skill-orchestration/references/composition-patterns-types.md`（隐式依赖最隐蔽：
⭐⭐⭐⭐⭐ **单独测试完全看不出来，只在生产"被单独调用"时暴露**）。
> ⭐⭐⭐⭐⭐ 选形态的依据不是"哪个更强大"，是⭐⭐⭐⭐ **哪个的失败点你能承受**——
> 扇出扇入最快，但它的失败点（部分成功）恰恰是最静默的那一种。

---

## 3. ⭐⭐⭐⭐⭐ 编排器：写还是不写

三条判据，全中才写：

```
① ⭐⭐⭐⭐⭐ 顺序必须强制（换一条路走你介意吗？介意才是编排器）
② ⭐⭐⭐⭐ 至少三个技能
③ ⭐⭐⭐⭐ 已经手动搬运过 3 次以上
```

> ⭐⭐⭐⭐⭐ 只中①不中②③ → ⭐⭐⭐⭐ **应该写成脚本或工作流，不是编排器**（顺序=确定性=该交给代码）。
> 编排器本身也是技能，遵守同样约束——**它也会过时、也会被跳步骤、也会有占位符**。
> ⭐⭐⭐⭐⭐ 常被忽略的推论：**编排器是链条上唯一"知道全局"的组件**，所以覆盖率、partial 传递、
> 失败定位只能由它负责——单个技能看不到别的技能。

---

## 4. ⭐⭐⭐⭐⭐ 扇出与扇入

| | 串行 | ⭐ 并行 |
|---|---|---|
| 失败时状态 | 卡在某步 | ⭐⭐⭐⭐⭐ N 个半成品 |
| 报错 | 一个 | ⭐⭐⭐⭐⭐ 可能 0 个 |

> ⭐⭐⭐⭐⭐ **N 个半成品：每个单独看都是成功的，合起来是错的，没有任何组件会报错。**
> 三条硬规则：① ⭐⭐⭐⭐⭐ 汇总必须报覆盖率（"3 个来源中 2 个成功，覆盖率 67%"）；
> ② ⭐⭐⭐⭐⭐ 部分成功必须传 partial，下游不得按全量处理；
> ③ ⭐⭐⭐⭐ 顺序敏感性测试：A→B 与 B→A 结果不同 → 禁止并行。**第③条的价值是不需要你事先知道依赖在哪。**

---

## 5. ⭐⭐⭐⭐⭐ 链式失败的形状

```
A → B → C 中 B 出错 → ⭐⭐⭐⭐⭐ C 的失败报告里根本不会提到 B
```

> ⭐⭐⭐⭐⭐ **出错的地方 ≠ 报错的地方。** 这是链式结构最贵的属性，也是它必须配可观测性的原因。

| 类型 | 表现 | ⭐ 关键点 |
|---|---|---|
| ⭐⭐⭐⭐⭐ 中间产物缺失 | 下游拿到空/旧文件 | 用"文件存在"判断"做过"是错的 |
| ⭐⭐⭐⭐⭐ 部分成功被当全成功 | 上游 2/3 成功，下游按全量处理 | `status: partial` 必须传递 |
| ⭐⭐⭐⭐⭐ 错误被逐级改写 | A 返回错误，B 当输入，C 输出"成功" | 每级都要显式检查上游状态 |

> ⭐⭐⭐⭐⭐ 第三种最危险：**每一级都在正常完成自己的工作，合起来把一个错误加工成了一份看起来成功的报告。**
> ⭐⭐⭐⭐⭐ 唯一的结构性对策是**每级显式检查上游状态**——不能靠"下游自然会发现问题"，
> 因为下游拿到的仍然是格式正确的输入。定位手段见 `skill-composition/references/chain-failure-localization.md`。

---

## 6. ⭐⭐⭐⭐⭐ 协议分层

```
MCP   = ⭐⭐⭐⭐⭐ 世界的形状（有什么能力）
技能   = ⭐⭐⭐⭐⭐ 做事的方法（怎么用这些能力）
编排器 = ⭐⭐⭐⭐ 什么时候用哪个
```

> ⭐⭐⭐⭐⭐ **MCP 是普通话，技能是方言。** 混淆的症状：把"有什么能力"写进技能 → 换个 MCP 就全错；
> 把"怎么用"写进 MCP → 能力被绑死在一个用法上。详见 `skill-composition/references/protocol-layering.md`。

---

## 7. 何时不用

```
Do NOT 用于：单技能内部的步骤顺序 · 技能之间传什么字段 · 决定触发哪一个技能
❌ ⭐⭐⭐⭐⭐ 顺序必须强制且只有一两个技能 —— 改用脚本或工作流
❌ 任务本身不稳定、每次流程都不同 —— 那是"对话"，不是链
```

> ⭐⭐⭐⭐⭐ 最后一条最容易误判：**流程每次都变说明还没沉淀出模式，写编排器会把"还没成形的东西"固化成结构。**

---

## 8. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ 报错的技能不是真正出错的技能 | `skill-orchestration/references/composition-patterns-types.md`（隐式依赖） |
| ⭐⭐⭐⭐⭐ 该不该写编排器 | `skill-orchestration/references/orchestrator-timing.md` |
| ⭐⭐⭐⭐⭐ 每层都在重试、总调用数失控 | `skill-composition/references/retry-amplification.md` |
| ⭐⭐⭐⭐⭐ 编排跑很久然后超时，没报错 | `skill-orchestration/references/dependency-cycles.md` |
| ⭐⭐⭐⭐ 技能互相读对方的临时字段 | `skill-interfaces/references/skill-data-passing.md` |
| ⭐⭐⭐⭐ 两个技能都要改同一份文件 | `skill-orchestration/references/collision-arbitration.md` |
| ⭐⭐⭐⭐ 汇总结果比预期少但不报错 | `skill-composition/references/partial-aggregation.md` |

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-composition/references/fan-out-fan-in.md` | ⭐⭐⭐⭐⭐ 扇出并行、汇总、覆盖率 |
| `skill-composition/references/partial-aggregation.md` | ⭐⭐⭐⭐⭐ 汇总的覆盖率、缺失偏差、分母来源 |
| `skill-composition/references/chain-failure-localization.md` | ⭐⭐⭐⭐⭐ 链路 ID、从后往前二分定位、每级检查上游状态 |
| `skill-composition/references/retry-amplification.md` | ⭐⭐⭐⭐⭐ 每层重试 3 次、三层链最坏 27 次；重试成功会抹掉失败记录 |
| `skill-composition/references/protocol-layering.md` | ⭐⭐⭐⭐ 协议分层原则 |
| `skill-composition/references/mcp-composition.md` | ⭐⭐⭐⭐ MCP 与技能的分层组合 |
| `skill-composition/references/skill-composition-patterns.md` | ⭐⭐⭐⭐ 组合的具体写法 |
| `skill-composition/references/sequential-composition.md` | ⭐⭐⭐⭐ 顺序链的产物传递、叠加加载 |
| `skill-composition/references/composable-patterns.md` | ⭐⭐⭐⭐ 可组合性设计 |
| `skill-composition/references/composition.md` | ⭐⭐⭐ 组合总览 |
