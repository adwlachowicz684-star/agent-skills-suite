# description 四条铁律（含中文场景）

> 相关：《skill-description》的 `imperative-description.md` ·
> `description-recipes.md` · 《skill-refining》的 `i18n.md`

---

## 目录

- [1. ⭐ 为什么 description 是唯一依据](#1--为什么-description-是唯一依据)
- [2. 铁律一：第三人称](#2-铁律一第三人称)
- [3. ⭐ 铁律二：触发词在前](#3--铁律二触发词在前)
- [4. ⭐ 铁律三：写明何时用与何时不用](#4--铁律三写明何时用与何时不用)
- [5. 铁律四：给 3–5 个真实触发例句](#5-铁律四给-35-个真实触发例句)
- [6. 官方口径补充](#6-官方口径补充)

---

## 1. ⭐ 为什么 description 是唯一依据

> ⭐ **description 是技能唯一被 AI 当作"判断要不要用"的依据。**
> AI 装了 100 个技能，**它不会读完所有 SKILL.md 才决定用哪个**——
> 它只看 name + description。

> ⭐ **description 写不好，再牛的技能也是死的。**

---

## 2. 铁律一：第三人称

```
❌ "帮你/我写一份周报..."
✅ "生成基于 git log 的周报，按业务价值排序，输出 markdown 格式。"
```

理由：

> ⭐ **description 会被注入到系统提示里，
> 第二人称会让 AI 错位。**

**官方口径**（更硬）：

```
Warning: Always write in third person.
The description is injected into the system prompt,
and inconsistent point-of-view can cause discovery problems.

Good:  "Processes Excel files and generates reports"
Avoid: "I can help you process Excel files"
Avoid: "You can use this to process Excel files"
```

> ⭐ 注意官方说的是 **"会导致发现问题"**（discovery problems）——
> 不只是风格问题，**会影响能否被找到**。

---

## 3. ⭐ 铁律二：触发词在前

```
❌ "一个非常智能的工具，能帮你处理各种任务，
    特别是当你需要审计 SQL 时..."
✅ "审计 SQL 注入和性能问题。当用户要求 review SQL、
    检查查询性能、或在 PR 涉及 .sql 文件时调用。"
```

> ⭐ 理由很硬：**description 经常会被截断，关键词必须在前面。**

这与 `budget-truncation.md` 那条一致——
**装太多技能时描述会被压缩以省字符预算，可能把匹配用的关键词削掉**。

---

## 4. ⭐ 铁律三：写明何时用与何时不用

```
❌ 模糊: "处理数据库相关任务"（AI 不知道该不该用）
✅ 清晰: "仅在用户要写新 SQL 查询时使用。
         不用于查看现有表结构（用 schema-viewer 技能）"
```

> ⭐ **"不用于 X（用 Y 代替）" 是最强的路由提示**——
> 与 `activation-rate.md` 的祈使句 + 否定约束、
> `namespace-collision.md` 的排除声明互相点名，完全同构。

---

## 5. 铁律四：给 3–5 个真实触发例句

放在 SKILL.md 正文开头：

```markdown
## 触发示例
- "帮我审一下这个查询"
- "看看这个 SQL 有没有注入风险"
- "这个 join 怎么优化"
```

> ⭐ **这是给 AI 看的"语义锚点"。
> 没有例句，AI 经常该用的时候不用、不该用的时候乱用。**

> ⭐ 注意位置：例句放**正文**（触发之后才加载），
> 而触发词放 **description**（决定要不要触发）。
> 两者分工不同——
> 正文例句的作用是**触发之后指导行为**，不是帮助触发。

---

## 6. 官方口径补充

**动名词命名**：

> ⭐ **建议技能名用动名词形式（verb + -ing）**，
> 因为它清楚地描述了技能提供的活动或能力。

（例：`Processing PDFs`、`Analyzing spreadsheets`）

**黄金公式**：

```
[做什么 What] + [何时触发 When to Trigger]  ≤1024 字符

❌ "A tool for documents"        —— 没说动作也没说触发
✅ "Extract text from PDFs. Use when user needs to process PDF files."
```

**反面清单**：

```
❌ "Helps with documents"
❌ "Processes data"
❌ "Does stuff with files"
```

---

## 速查

| 铁律 | 关键词 |
|---|---|
| ① 第三人称 | ⭐ 会被注入系统提示，第二人称导致发现问题 |
| ② 触发词在前 | ⭐ 会被截断 |
| ③ 何时用 + 何时不用 | ⭐ "不用于 X（用 Y）" 最强 |
| ④ 3–5 个例句 | ⭐ 语义锚点，放正文 |

```
□ 第三人称（不用"我/你"）
□ ⭐ 关键词在开头（防截断）
□ 有"不用于 X（用 Y 代替）"
□ ⭐ 正文有 3–5 个真实触发例句
□ ≤1024 字符
□ 动名词命名（可选但推荐）
```

**中文场景补充**：
中文日常表达更丰富，同一件事至少五种说法——
**把所有你同事会说的说法都写进 description**
（详见《skill-refining》的 `i18n.md`）。
