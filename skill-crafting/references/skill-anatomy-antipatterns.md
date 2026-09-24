# 技能解剖：结构、五种反模式、发布前五测

> 相关：《skill-crafting》的 `anti-patterns-catalog.md` ·
> `common-mistakes-checklist.md` · 《skill-structuring》的
> `frontmatter-pitfalls.md`
> 前置：`anti-patterns-catalog.md` 是按"类别"归的反模式，
> 这份按⭐ **"一个技能的完整解剖 + 五个具名反模式 + 发布前五测"**组织。

---

## 目录

- [1. ⭐ 核心原则一句话](#1--核心原则一句话)
- [2. 官方解剖结构](#2-官方解剖结构)
- [3. ⭐⭐ 五个具名反模式](#3--五个具名反模式)
- [4. ⭐ 发布前五测](#4--发布前五测)
- [5. ⭐⭐ description 里绝不要总结工作流](#5--description-里绝不要总结工作流)

---

## 1. ⭐ 核心原则一句话

> ⭐⭐ **description 触发它，正文教它。**
>
> ```
> description 告诉 agent ⭐ 什么时候用（WHEN）
> 正文       告诉 agent ⭐ 怎么执行（HOW）
> ```

---

## 2. 官方解剖结构

```yaml
---
name: [小写连字符名]
description: [具体动作 + "Use when..." 从句]
version: [语义化版本]
triggers:
  - [关键词 1]
tags:
  - [标签]
---

# [技能标题]

[介绍段落：说明目的]

## Core Principle
**[用粗体标出的最重要的一条规则]**

## [主要内容章节]

## [决策点]

## Verification Checklist
```

**字段约束**：

| 字段 | 必需 | 约束 |
|---|---|---|
| name | ✅ | 小写字母+数字+连字符，1–64 字符 |
| description | ✅ | ⭐ 必须含 "Use when..." 从句，1–1024 字符 |
| version | ✅ | 语义化版本 |
| triggers | 建议 | ⭐ 自然语言短语 |
| tags | 建议 | 分类标签 |

**写触发词的三条**（好坏对照很清楚）：

```
✅ "write tests first" / "tdd" / "test driven development"
❌ "testing methodology"                    （太泛）
❌ "red-green-refactor-cycle-for-tdd"       （太具体）
❌ "skill-123"                              （不是自然语言）
```

> ⭐ 判据就是：**一个真人会怎么问？**

---

## 3. ⭐⭐ 五个具名反模式

| 反模式 | 问题 | 修法 |
|---|---|---|
| **The Encyclopedia**（百科全书） | 信息太多，agent 迷路 | ⭐ 只保留可行动的指引 |
| **The Vague Guide**（含糊指南） | "Consider best practices" | ⭐ 具体化："Use Arrange-Act-Assert" |
| **The Constraint-Free Skill** | 没有清晰规则，agent 即兴发挥 | ⭐ 加入显式约束 |
| **The Monologue**（独白） | 一整面文字墙 | ⭐ 用标题、列表、表格、代码块 |
| **The Outdated Skill** | 引用了已废弃的模式 | ⭐ 做版本管理并定期复查 |

> ⭐ 第二个的反例特别好："Consider best practices" → "Use Arrange-Act-Assert"
> ——**把原则换成具体做法**，与《patterns》里"禁令要带 Instead"同源。

**指令强度的两种档位**（什么时候用哪个）：

```
强（关键规则）："You MUST…" / "ALWAYS…" / "NEVER…" / "Do NOT…"
软（建议）    ："Prefer…" / "Consider…" / "When possible…"
```

**决策点的写法**（一个可复制的模板）：

```markdown
## Decision: [要决定什么]

If [条件 A]: → [A 的动作]
If [条件 B]: → [B 的动作]
If uncertain: → ⭐ [默认动作]
```

> ⭐ **"If uncertain" 这一行必须有**——
> 没有默认分支，模型在边界情形就会即兴发挥。

**步骤写作的模板**：

```markdown
### Step 1: [动作]
[详细说明]
**Verification:** [怎么知道这一步完成了]
```

> ⭐ "Verification" 那行是关键：
> 它把"做完"变成**可判定的**，与《evaluating》的
> "断言打在环境状态上"是同一条原则写进了正文。

---

## 4. ⭐ 发布前五测

```
① 触发测试     — 它会在预期的说法上激活吗？
② 完整性测试   — agent 能不靠外部信息就照着做吗？
③ 清晰度测试   — 每条指令都无歧义吗？
④ ⭐ 矛盾测试  — 有没有互相冲突的指引？
⑤ 边界测试     — 能处理异常/不常见的情形吗？
```

> ⭐ 第 ④ 条最容易被跳过，而它恰恰是
> `skillsbench-vs-realworld.md` 里"负增益任务"的主要成因——
> **技能引入了互相冲突的指引**。

---

## 5. ⭐⭐ description 里绝不要总结工作流

> ⭐⭐ **绝不在 description 里总结技能的工作流。**
> ⭐ **Claude 可能照着 description 抄近路，而不去读完整的正文。**

**对照**：

```
❌ 坏（描述了工作流）：
   "Fetches PR, groups comments, presents summary,
    lets user select fixes."
   ⭐ 模型看到这段就可能直接照做，跳过正文里的关键约束

✅ 好（WHAT + WHEN + 触发词）：
   "Reviews code changes for bugs, performance issues,
    and security problems. Use when reviewing PRs,
    before committing, or when user asks to review code."
```

> ⭐⭐ 这是我在整个收藏里见过**最反直觉也最实用**的一条写作规则：
> **把 description 写得"信息更全"反而可能有害**，
> 因为它给了一条绕开正文的捷径。

**配套的四条"不要包含"**：

```
❌ 安装章节        —— 技能通过 description 自动发现
❌ 正文里的 "When to Use" 章节
   ⭐⭐ 这个属于 description！⭐ 正文是在触发之后才加载的，
   ⭐ 写在这里等于马后炮
❌ README 或 changelog —— 只留 SKILL.md 和可选 reference
❌ hook 设置        —— hooks 是另一套系统，不属于技能
```

**推荐的起步体量**：

```
⭐ 多数技能 <300 行
⭐ 参考数据用表格而非散文
⭐ 引用其他技能时⭐ 只写名字，不复制其内容
```

**一个便宜的验收招**：

```
⭐ 发布前用一个干净的子代理测试：
   Task(subagent_type="general-purpose", model="haiku"):
   "读 [技能路径] 并评估：
    1. description 质量（WHAT + WHEN + 触发词、第三人称、<1024 字符）
    2. 命名（动名词形式）
    3. 没有安装章节
    4. 完整性——有缺口吗？
    5. token 效率——有冗余吗？"
```

> ⭐ 用 haiku 跑这步又快又便宜——
> 而且有个额外好处：**如果连 haiku 都能看懂，
> 说明指令足够显式**（呼应 `anti-patterns-catalog.md` 的
> "对 Haiku 要解释更充分"）。

---

## 速查

```
□ ⭐⭐ description 触发它，正文教它
□ name：小写+数字+连字符，≤64 字符
□ ⭐ description 必须含 "Use when..." 从句
□ 触发词：真人会怎么问？（不用太泛/太具体/非自然语言）
□ 结构：介绍 → Core Principle（粗体一条）→ 内容 → 决策点 → 清单
□ ⭐ 决策点必须有 "If uncertain" 默认分支
□ ⭐ 每个 Step 带 **Verification:** 行

⭐ 五个反模式：
□ Encyclopedia（太多）→ 只留可行动的
□ Vague Guide → 具体化（"Use Arrange-Act-Assert"）
□ Constraint-Free → 加显式约束
□ Monologue（文字墙）→ 标题/列表/表格/代码块
□ Outdated → 版本管理 + 定期复查

发布前五测：
□ 触发 / 完整性 / 清晰度 / ⭐矛盾 / 边界

⭐⭐ 写作红线：
□ ⭐ 绝不在 description 里总结工作流（会抄近路跳过正文）
□ ⭐ 正文里不要有 "When to Use" 章节（那是 description 的活）
□ 不要安装章节、README、changelog、hook 设置

□ ⭐ 多数技能 <300 行；引用其他技能只写名字不复制
□ ⭐ 用 haiku 子代理做验收，又快又便宜
```

**一句话**：

> ⭐⭐ **把 description 写得越"完整"，越可能给模型一条绕开正文的捷径——
> 所以 summary 式的 description 有害。**
