# 参考文件的组织与拆分阈值

> 相关：`skill-structuring` 的 `progressive-disclosure-official.md`（三模式）·
> `skill-structuring` 的 `reference-routing.md` · `skill-structuring` 的 `references-vs-assets.md`

---

## 目录

- [1. 目标尺寸](#1-目标尺寸)
- [2. ⭐ 何时拆](#2--何时拆)
- [3. 三种组织方式](#3-三种组织方式)
- [4. ⭐ 大文件要配 grep 模式](#4--大文件要配-grep-模式)
- [5. ⭐ 可发现的描述](#5--可发现的描述)
- [6. 参考文件的 frontmatter](#6-参考文件的-frontmatter)
- [7. 避免循环依赖](#7-避免循环依赖)

---

## 1. 目标尺寸

| 对象 | 目标 |
|---|---|
| **SKILL.md 正文** | ⭐ 1,500–2,000 词 |
| **单个参考文件** | < 10,000 词 |
| **技能总大小** | 无硬限制，但很大时应考虑拆成多个技能 |

> 另一处口径：SKILL.md 控制在 **8–15K 字符**。
> 两者一致（1,500–2,000 词 ≈ 8–15K 字符，中文按字符算）。

---

## 2. ⭐ 何时拆

满足任一条件就拆：

```
① 超过 10,000 词
② ⭐ 覆盖多个不同主题
③ ⭐ 不同任务需要不同章节
```

示例：

```
拆前：references/api-reference.md（15,000 词）
拆后：references/api-authentication.md
     references/api-endpoints.md
     references/api-errors.md
```

> ⭐ 第 ③ 条最实用——**按"谁需要哪一段"来切**，
> 而不是按字数平均切。

---

## 3. 三种组织方式

| 方式 | 适用 | 例子 |
|---|---|---|
| **按主题** | 领域知识 | authentication / authorization / data-models / api-endpoints |
| ⭐ **按任务类型** | 操作型 | creating-resources / querying-data / handling-errors / testing-patterns |
| **按复杂度** | 学习曲线 | getting-started / common-patterns / advanced-techniques / edge-cases |

> ⭐ **按任务类型**最贴合"按需加载"——
> 因为模型的需要通常是"我现在要做什么"，而不是"这属于哪个主题"。

---

## 4. ⭐ 大文件要配 grep 模式

> ⭐ **超过 5,000 词的参考文件，在 SKILL.md 里给出 grep 模式。**

```markdown
数据库 schema 详见 `references/schemas.md`。搜索模式：
- 用户表：`grep -n "## User" references/schemas.md`
- 订单表：`grep -n "## Order" references/schemas.md`
```

这与 `skill-structuring` 的 `references-vs-assets.md` 那条（>1 万词给 grep 模式）一致，
只是阈值更严（5,000 词）。取严的那个。

---

## 5. ⭐ 可发现的描述

Claude 通过四种途径发现参考文件：

```
① SKILL.md 里的明确提及    "See references/patterns.md"
② ⭐ frontmatter 描述      读描述判断相关性
③ 目录列举                 列出 references/ 目录
④ 交叉引用                 文件间的链接引导导航
```

**好描述 vs 坏描述**：

```yaml
# ✅ 好
description: Database schema reference for the user management system.
             Load when working with user tables, authentication, or permissions queries.

# ❌ 坏
description: Schema reference.
```

> ⭐ 差别在于**有无加载条件**。
> "Load when…" 是给模型的路由信号，与技能描述同理。

---

## 6. 参考文件的 frontmatter

参考文件本身也可以有结构化 frontmatter：

```yaml
---
name: database-schemas
title: Database schema reference
description: Complete schema documentation...
  Load when writing queries, creating migrations, or debugging data issues.
commands:
  psql -d mydb -c "\dt": List all tables
principles:
  - All tables use UUID primary keys
  - Timestamps are stored in UTC
checklist:
  - Foreign keys have appropriate indexes
related:
  - migrations
  - queries
---
```

> ⭐ `principles` 和 `checklist` 这两个字段很值得抄——
> 它们把"约定"和"验收"结构化，而不是藏在散文里。

---

## 7. 避免循环依赖

> ⭐ 尽量让每份参考文件**自包含**。
> 如果 A 引用 B、B 又引用 A，确保各自都能被独立理解。

循环依赖会让人（和模型）都无法确定从哪开始读。

---

## 速查

| 事 | 阈值/做法 |
|---|---|
| SKILL.md | 1,500–2,000 词 / 8–15K 字符 |
| 单文件上限 | 10,000 词 |
| 拆的判据 | ⭐ 多主题 / 不同任务需要不同章节 |
| 组织方式 | ⭐ 优先按任务类型 |
| >5,000 词 | ⭐ 配 grep 模式 |
| 描述 | ⭐ 必须带 "Load when…" |
| 引用 | 避免循环 |
