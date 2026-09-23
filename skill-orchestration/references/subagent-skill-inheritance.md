# 子代理不继承技能（以及内置 agent 完全用不了）

> 相关：《skill-orchestration》的 `subagents.md` ·
> `skill-subagent-combo.md` · `subagent-teams.md` ·
> `fork-official-details.md`

---

## 目录

- [1. ⭐ 一个让很多人意外的行为](#1--一个让很多人意外的行为)
- [2. 三条必须分清的区别](#2-三条必须分清的区别)
- [3. 正确配置方式](#3-正确配置方式)
- [4. ⭐ 加载时机：启动时，不是按需](#4--加载时机启动时不是按需)
- [5. 什么时候用这个模式](#5-什么时候用这个模式)

---

## 1. ⭐ 一个让很多人意外的行为

> ⭐ **子代理不会自动看到你的技能。**
> 委派任务给子代理时，它从**全新的、干净的上下文**开始。

这是委派类故障里最常见也最难自查的一个：
**主对话里技能明明能用，一委派就失效**——因为对方根本没带。

---

## 2. 三条必须分清的区别

| | 能否用技能 |
|---|---|
| ⭐ **内置 agent**（Explorer / Plan / Verify） | ⭐ **完全不能访问技能** |
| **自定义子代理**（`.claude/agents` 里定义的） | 能，但⭐ **必须在 frontmatter 显式列出** |
| 主对话 | 按需加载 |

> ⭐ **只有你自己在 `.claude/agents` 里定义的子代理能用技能。**
> 想让 Explore 用你的技能——做不到，没有配置项能改。

---

## 3. 正确配置方式

在 `.claude/agents` 里加一个 agent markdown 文件
（可用 `/agents` 命令交互式创建）：

```yaml
---
name: frontend-security-accessibility-reviewer
description: "Use this agent when you need to review frontend code for accessibility..."
tools: Bash, Glob, Grep, Read, WebFetch, WebSearch, Skill...
model: sonnet
color: blue
skills: accessibility-audit, performance-check
---
```

> 委派给这个子代理时，**两个技能都已加载，并应用到每一次审查**。

**前提**：确保这些技能先存在于 `.claude/skills`，
然后要么新建子代理，要么给已有 agent 文件加上 `skills` 字段。

---

## 4. ⭐ 加载时机：启动时，不是按需

> ⭐ **子代理里的技能在子代理启动时加载，
> 不像主对话那样按需加载。**

含义很实在：

```
✅ 常用、确定要用的技能 → 放子代理 skills 字段（启动即就绪）
❌ 偶尔用一次的大技能  → ⭐ 会让每次启动都付出成本
```

> 这是 `composition.md` 里"预加载 vs 按需"取舍的一个具体实现约束。
> 子代理的 `skills` 字段**没有按需这一档**。

---

## 5. 什么时候用这个模式

```
① 想要带特定专长的隔离任务委派
② ⭐ 不同子代理需要不同技能（前端审查 vs 后端审查）
③ 同一个子代理要稳定应用同一套标准
```

> 价值在于：
> ⭐ **把"只在 Alice 机器上管用的巧妙配置"
> 变成"装上这个，所有人按同一标准工作"。**

---

## 速查

| 现象 | 原因 |
|---|---|
| 委派后技能失效 | ⭐ 子代理不继承，要显式列 `skills:` |
| 想让 Explore 用技能 | ⭐ 做不到——内置 agent 完全不能访问 |
| 启动变慢 | `skills:` 是启动时全量加载 |
| 多团队技能冲突 | ⭐ 用插件命名空间 `/plugin:skill` |

| 要做 | |
|---|---|
| ✅ 自定义子代理 + `skills:` 字段 | |
| ✅ 技能先存在于 `.claude/skills` | |
| ✅ 常用技能才放进 `skills:` | |
| ❌ 指望内置 agent 能读技能 | |
