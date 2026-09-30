---
name: skill-composition
description: 多个技能按什么形状组合——顺序链、扇出扇入、条件分支、流水线，以及编排器该不该写、协议分层（MCP 是普通话，技能是方言）。用于「几个技能怎么搭」「要不要写编排器」「要不要并行」「MCP 与技能职责怎么分」。不用于该不该链（见 skill-chaining）、技能间字段契约（见 skill-interfaces）、触发哪个技能（见 skill-orchestration）。
license: MIT
---

# 技能组合：把几个技能搭成一个形状

> 前置：《skill-chaining》（该不该串、链式失败的形状）·
> 《skill-interfaces》（技能间传什么）
> 分工：
> 《skill-chaining》管⭐⭐⭐⭐⭐ **要不要串、串了怎么坏**；
> 本技能管⭐⭐⭐ **串成什么形状、以及这个形状怎么写**；
> 《skill-interfaces》管⭐⭐⭐⭐ **它们之间传什么**。

---

## 目录

- [1. 组合的四种形态](#1-组合的四种形态)
- [2. ⭐⭐⭐⭐⭐ 编排器：写还是不写](#2--编排器写还是不写)
- [3. ⭐⭐⭐⭐⭐ 扇出与扇入](#3--扇出与扇入)
- [4. ⭐⭐⭐⭐⭐ 协议分层](#4--协议分层)
- [5. 速查](#5-速查)

---

## 1. 组合的四种形态

| 形态 | 结构 | ⭐ 失败点 |
|---|---|---|
| 顺序链 | A → B → C | ⭐⭐⭐⭐ 中间产物 |
| ⭐⭐⭐⭐⭐ 扇出扇入 | A → {B,C,D} → 汇总 | ⭐⭐⭐⭐⭐ 部分成功 |
| ⭐⭐⭐⭐ 条件分支 | 按输入选一条 | ⭐⭐⭐⭐ 分支未覆盖输入 |
| ⭐⭐⭐ 流水线 | 每级产出一个产物 | ⭐⭐⭐⭐⭐ 错误被逐级改写 |

依赖类型与三个反模式见 `skill-orchestration/references/composition-patterns-types.md`（隐式依赖最隐蔽：
⭐⭐⭐⭐⭐ **单独测试完全看不出来，只在生产"被单独调用"时暴露**）。

> ⭐⭐⭐⭐⭐ 选形态的依据不是"哪个更强大"，是⭐⭐⭐⭐ **哪个的失败点你能承受**。
> 扇出扇入最快，但它的失败点（部分成功）恰恰是最静默的那一种。

---

## 2. ⭐⭐⭐⭐⭐ 编排器：写还是不写

三条判据，全中才写：

```
① ⭐⭐⭐⭐⭐ 顺序必须强制（换一条路走你介意吗？介意才是编排器）
② ⭐⭐⭐⭐ 至少三个技能
③ ⭐⭐⭐⭐ 已经手动搬运过 3 次以上
```

> ⭐⭐⭐⭐⭐ 只中①不中②③ → ⭐⭐⭐⭐ **应该写成脚本或工作流，不是编排器**。
> 这与"顺序=确定性=该交给代码"是同一条原则。

编排器本身也是技能，遵守同样约束（**它也会过时、也会被跳步骤、也会有占位符**）。

> ⭐⭐⭐⭐ 一个常被忽略的推论：⭐⭐⭐⭐⭐ **编排器是链条上唯一"知道全局"的组件**，
> 所以覆盖率、partial 传递、失败定位只能由它负责——单个技能看不到别的技能。

---

## 3. ⭐⭐⭐⭐⭐ 扇出与扇入

并行让失败形状变了：

| | 串行 | ⭐ 并行 |
|---|---|---|
| 失败时状态 | 卡在某步 | ⭐⭐⭐⭐⭐ N 个半成品 |
| 报错 | 一个 | ⭐⭐⭐⭐⭐ 可能 0 个 |

> ⭐⭐⭐⭐⭐ **N 个半成品：每个单独看都是成功的，合起来是错的，没有任何组件会报错。**

三条硬规则：

```
① ⭐⭐⭐⭐⭐ 汇总时必须报覆盖率（"3 个来源中 2 个成功，覆盖率 67%"）
② ⭐⭐⭐⭐⭐ 部分成功必须传 partial，下游不得按全量处理
③ ⭐⭐⭐⭐ 顺序敏感性测试：A→B 与 B→A 结果不同 → 禁止并行
```

第 ③ 条的价值在于：**不需要你事先知道依赖在哪**。

---

## 4. ⭐⭐⭐⭐⭐ 协议分层

```
MCP     = ⭐⭐⭐⭐⭐ 世界的形状（有什么能力）
技能     = ⭐⭐⭐⭐⭐ 做事的方法（怎么用这些能力）
编排器   = ⭐⭐⭐⭐ 什么时候用哪个
```

> ⭐⭐⭐⭐⭐ **MCP 是普通话，技能是方言。**
> 混淆这两层的典型症状：把"有什么能力"写进技能 → 换个 MCP 就全错；
> 把"怎么用"写进 MCP → 能力被绑死在一个用法上。

组合模式与失败不对称见 `skill-composition/references/mcp-composition.md` 与 `skill-composition/references/protocol-layering.md`。

---

## 5. 速查

| 症状 | 先看 |
|---|---|
| ⭐⭐⭐⭐⭐ 并行后结果变少但不报错 | `skill-composition/references/fan-out-fan-in.md` |
| ⭐⭐⭐⭐⭐ MCP 与技能职责混淆 | `skill-composition/references/mcp-composition.md` |
| ⭐⭐⭐⭐ 顺序链产物传递 | `skill-composition/references/skill-chaining-composition.md` |
| ⭐⭐⭐⭐ 想让技能能被别人组合 | `skill-composition/references/composable-patterns.md` |
| ⭐⭐⭐ 组合总览 | `skill-composition/references/composition.md` |

---

## 路由表

| 参考文件 | 何时读 |
|---|---|
| `skill-composition/references/fan-out-fan-in.md` | ⭐⭐⭐⭐⭐ 扇出并行、汇总、覆盖率 |
| `skill-composition/references/protocol-layering.md` | ⭐⭐⭐⭐ 协议分层原则 |
| `skill-composition/references/mcp-composition.md` | ⭐⭐⭐⭐ MCP 与技能的分层组合 |
| `skill-composition/references/skill-composition-patterns.md` | ⭐⭐⭐⭐ 组合的具体写法 |
| `skill-composition/references/skill-chaining-composition.md` | ⭐⭐⭐⭐ 顺序链的产物传递 |
| `skill-composition/references/composable-patterns.md` | ⭐⭐⭐⭐ 可组合性设计 |
| `skill-composition/references/composition.md` | ⭐⭐⭐ 组合总览 |
