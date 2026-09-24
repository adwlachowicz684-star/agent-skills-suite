# 祈使句而非第二人称：为什么这不是语法洁癖

> 相关：《skill-authoring》的 `writing-style.md` ·
> `description-writing.md` · 《skill-patterns》的 `instruction-craft.md`

---

## 目录

- [1. ⭐ 正文：祈使句](#1--正文祈使句)
- [2. ⭐ description：第三人称](#2--description第三人称)
- [3. 两者的共性](#3-两者的共性)
- [4. ⭐ 尺寸分级](#4--尺寸分级)
- [5. 质量评分里的权重](#5-质量评分里的权重)

---

## 1. ⭐ 正文：祈使句

```
❌ 第二人称：You should start by reading the configuration file.
✅ 祈使语气：Start by reading the configuration file.
```

```
❌ You should create the directory.
❌ You need to validate the frontmatter.
❌ Check if the fields are there.

✅ Create the skill directory structure.
✅ Validate the YAML frontmatter.
✅ Check for required fields.
```

**三个理由**（都很实在，不是口味问题）：

```
① ⭐ 直接下达动作，比 "You should…" 更干脆
② ⭐ 更省 token
③ ⭐ ⭐ 不会有代词指向的歧义
```

> ⭐ 第 ③ 条最关键：**"you" 在一段被注入另一个 agent 上下文的指令里，
> 指代是不确定的**——是指 agent？指用户？指下一段里的某个角色？

**根本原因**：正文不是给人看的说明书，**是写给"另一个 agent 实例去执行的操作手册"**。

---

## 2. ⭐ description：第三人称

```
❌ 第一人称：I can help you analyze LLM traces...
✅ ⭐ 第三人称：This skill should be used when the user asks to "debug a trace"...
```

**好例子**（含具体触发短语）：

```yaml
description: >
  Debug and inspect LLM/AI agent traces using PostHog's MCP tools.
  Use when the user pastes a trace URL, asks to debug a trace,
  figure out what went wrong, check if an agent used a tool correctly...
```

**坏例子**：

```
❌ 'Helps with AI observability'            —— 太含糊，判断不出何时用
❌ 'Everything about PostHog AI features'   —— ⭐ 太宽，一把伞不是技能
```

> ⭐ **规则：description 要客观陈述触发条件，正文要直接下达操作指令。
> ⭐ 两者都不要用 "you" 制造指向不清的歧义。**

---

## 3. 两者的共性

```
description  → 第三人称，客观陈述"什么时候用"
正  文       → 祈使句，直接下达"怎么做"
```

**正文通常回答三个问题**：

```
① 这个技能干什么
② 什么时候用（⭐ 主要放 description）
③ 具体怎么用
```

> ⭐ **第 ③ 条里有个硬要求：
> ⭐ "怎么用"必须明确引用所有 scripts / references / assets，
> ⭐ 否则 agent 根本不知道这些资源存在。**

---

## 4. ⭐ 尺寸分级

按加载频率设定目标：

```
会话启动技能   <150 字
高频技能       <200 字
其他技能       <500 字
```

| 位置 | 尺寸目标 |
|---|---|
| 触发元数据（frontmatter） | ⭐ 合并 description + when_to_use ≤ 1,536 字符，会被截断 |
| ⭐ 核心指令（SKILL.md 正文） | ⭐ **1,500–2,000 词** |
| 详细参考（references/*.md） | 2,000–5,000 词/份 |
| 模板（templates/） | 按需 |
| 脚本（scripts/） | 按需 |

> ⭐ **绝不要把 5,000 词的参考文档放进 SKILL.md 正文。**
> 移到 references/ 并加一行：
> "For detailed X, read ${CLAUDE_SKILL_DIR}/references/x.md."

**前置加载的硬约束**：

```
⭐ description + when_to_use 合计上限 1,536 字符，超出会被截断
→ ⭐ ⭐ 重要的触发词放在末尾可能直接被切掉
→ ⭐ 把主要用例前置（front-load）
```

---

## 5. 质量评分里的权重

一个可用的四维加权：

```
Overall = Description×0.25 + Organization×0.30 + Style×0.20 + Structure×0.25
```

**写作风格维（20%）内部**：

```
祈使句形式              40 分   全程动词开头
⭐ 正文中不使用第二人称   30 分   避免对话式的第二人称
客观语言                30 分   事实性、指导性语气
```

**渐进式披露维（30%）**：

```
SKILL.md 简洁、细节在 references/   30
SKILL.md 长度 <5,000 字（1,500–2,000 理想）  25
references/ 使用情况                 25
逻辑组织                             20
```

**结构完整性维（25%）**：

```
YAML frontmatter 30 · 目录结构 30 · ⭐ 资源引用 40（⭐ 被引用的文件确实存在）
```

等级映射：97–100 A+ · 90–92 A- · 80–82 B- · 70–72 C- · <60 F。

---

## 速查

```
正文：
□ ⭐ 祈使句，动词开头
□ ⭐ 不用 you / you should / you need
□ 更干脆 + 更省 token + ⭐ 无代词歧义
□ ⭐ 必须显式引用 scripts/references/assets

description：
□ ⭐ 第三人称（"This skill should be used when..."）
□ 不用第一人称
□ 含具体触发短语
□ ⭐ 主要用例前置（防 1,536 字符截断）

尺寸：
□ 会话启动 <150 字 · 高频 <200 · 其他 <500
□ ⭐ 正文 1,500–2,000 词
□ ⭐ 参考文件 2,000–5,000 词/份
□ ⭐ 绝不放 5,000 词文档进正文
□ ⭐ 引用用 ${CLAUDE_SKILL_DIR}/references/x.md

评分：
□ Description 25% / Organization 30% / Style 20% / Structure 25%
□ ⭐ 资源引用占结构维 40 分（被引用的文件必须存在）
```

**一句话**：

> ⭐ **不是语法洁癖——"you" 在一段被注入另一个上下文的指令里，指代是不确定的。**
