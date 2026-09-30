---
name: skill-subagents
description: 子代理与 fork 隔离环境下的技能使用。当需要决定"任务该不该放到隔离上下文里跑"（子代理 vs 技能、fork 的 token 经济学、子代理继承什么、并行子代理、多代理评审）时使用。含 skill+subagent 组合模式与上下文隔离的代价。
  Do NOT use for 技能之间的编排与依赖（用 skill-orchestration）、MCP 与工具的边界（用 skill-boundaries）、安全沙箱与权限（用 skill-security）。
---

# 子代理与 fork 隔离

## 边界

- 用于：**任务在哪个上下文里执行**——子代理、fork、并行、隔离
- 不用于：技能之间的编排 → 《skill-orchestration》
- 不用于：MCP vs 技能 → 《skill-boundaries》
- 不用于：权限与沙箱 → 《skill-security》

## 核心原则

> ⭐⭐⭐⭐⭐ **判断轴是隔离，不是大小。**
> ❌ "任务看起来很大 → 子代理"
> ✅ "这个任务会因为看不到其余对话而受益吗？"

```
□ ⭐⭐⭐⭐⭐ 子代理决定工作在哪里发生
□ ⭐⭐⭐⭐⭐ 技能决定它到了那里之后怎么做才算做好
□ ⭐⭐⭐⭐⭐ 强模式 = 派子代理 + 给它挂技能
   ⭐⭐⭐⭐⭐ 不显式挂技能，你的子代理就是在裸奔
□ ⭐⭐⭐⭐⭐ 技能内容会变成子代理的提示词
   → ⭐⭐⭐⭐⭐ 只写准则的 fork 技能 = 空输出（最常见的错误）
```

## 路由表

| `skill-subagents/references/skill-vs-subagent.md` | ⭐⭐⭐⭐⭐ 判断轴是隔离不是大小；⭐⭐⭐⭐ 按"大小"判断会导致把需要上下文的大任务丢给子代理，答案反而变差 |
| `skill-subagents/references/context-isolation-fork.md` | ⭐⭐⭐⭐⭐ 隔离扔掉的可能正是任务需要的信息 |
| `skill-subagents/references/fork-token-economics.md` | ⭐⭐⭐⭐⭐ 主上下文成本零，fork 内仍加载完整正文；⭐⭐⭐⭐ fork 必须共享父前缀 |
| `skill-subagents/references/fork-official-details.md` | ⭐⭐⭐⭐⭐ 子代理打破整个层叠：②③ 两层默认不存在 |
| `skill-subagents/references/fork-context-skill.md` | ⭐⭐⭐⭐ 子代理内技能可用性 |
| `skill-subagents/references/subagent-skill-inheritance.md` | ⭐⭐⭐⭐⭐ 继承什么、不继承什么 |
| `skill-subagents/references/subagent-advanced.md` | ⭐⭐⭐⭐ 高级用法 |
| `skill-subagents/references/subagent-teams.md` | ⭐⭐⭐⭐ 多代理分工 |
| `skill-subagents/references/skill-subagent-combo.md` | ⭐⭐⭐⭐ 组合模式 |
| `skill-subagents/references/parallel-subagents.md` | ⭐⭐⭐⭐⭐ N 个半成品：每个单独看都成功，合起来是错的 |
| `skill-subagents/references/multi-agent-review.md` | ⭐⭐⭐⭐ 评审型多代理 |
| `skill-subagents/references/subagents.md` | ⭐⭐⭐ 基础 |

## Critical Rules

- ⭐⭐⭐⭐⭐ **派子代理时必须显式挂技能**，否则它在裸奔
- ⭐⭐⭐⭐⭐ fork 型技能正文必须写成一份独立可执行的工单（读哪些文件、查什么、返回什么）
- ⭐⭐⭐⭐⭐ 子代理打破层叠——调试要查"子代理收到了什么"，不是"父代理有什么"
- ⭐⭐⭐⭐⭐ 并行把失败变成 N 个半成品且不报错
- ⭐⭐⭐⭐ fork 必须共享父前缀，否则对话越长那次调用越贵

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "任务太大，用子代理" | ⭐⭐⭐⭐⭐ 判据是隔离收益，不是大小 |
| "子代理自己会找技能" | ⭐⭐⭐⭐⭐ 不会。不显式挂就是在裸奔 |
| "fork 技能写个准则就行" | ⭐⭐⭐⭐⭐ 正文就是子代理的提示词，准则 ≠ 任务 → 输出为空 |
| "并行更快" | ⭐⭐⭐⭐⭐ 无序并行可能比只跑一个还差 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验 |
| `scripts/estimate_tokens.py <dir>` | 成本估算 |

## 参考

- 相关技能：《skill-orchestration》（编排与依赖）·《skill-boundaries》（MCP 边界）·
  《skill-security》（权限与沙箱）·《skill-selection》（库存与成本）
