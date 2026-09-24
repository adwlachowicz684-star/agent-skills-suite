# 五个立刻能做的起步技能（含完整源码）

> 相关：《skill-crafting》的 `first-skill-minimal.md` ·
> `official-templates.md` · 《skill-authoring》的 `how-to-guide.md`

---

## 目录

- [1. 为什么从这五个开始](#1-为什么从这五个开始)
- [2. 代码审查](#2-代码审查)
- [3. ⭐ Commit Message 生成器](#3--commit-message-生成器)
- [4. PR 描述](#4-pr-描述)
- [5. 调试助手](#5-调试助手)
- [6. 测试生成器](#6-测试生成器)
- [7. 文档生成器](#7-文档生成器)
- [8. 五条实战提示](#8-五条实战提示)

---

## 1. 为什么从这五个开始

这五个都是**高频、重复、规则清晰**的任务——
正是 `cold-start.md` 说的理想起步点。

> ⭐ **从一个你反复面对的真实问题开始。
> 一个专注、把一件事做好的技能，永远胜过一个大而全的。**

---

## 2. 代码审查

```yaml
---
name: code-review
description: Review code changes for bugs, security issues, and style
---
```

正文要点：

```
审查当前 git diff，给出：
1. Bugs        —— 逻辑错误、边界情况、null 检查
2. Security    —— SQL 注入、XSS、代码里的密钥
3. Performance —— N+1 查询、多余循环、内存泄漏
4. Style       —— 命名、结构、可读性
5. Tests       —— 缺失的测试用例

每个问题给出：文件与行号 · 错在哪 · 怎么修（带代码）
```

> ⭐ 最后两句是关键写法：
> **"Be concise. Skip praise. Only flag real issues."**
> 明确禁止赞美，否则输出会被客套稀释。

---

## 3. ⭐ Commit Message 生成器

```yaml
---
name: commit
description: Generate conventional commit messages from staged changes
---
```

```
看 git diff --staged，按 Conventional Commits 写提交信息：
type(scope): description
Types: feat, fix, docs, style, refactor, test, chore
首行不超过 72 字符。改动复杂时加正文。
```

> ⭐ 这类**偏好型技能**（见 `capability-vs-preference.md`）
> 最适合起步——规则明确、验收简单、模型升级也不易破坏。

---

## 4. PR 描述

```
用 git log main..HEAD 和 git diff main...HEAD 对比当前分支与 main。
写出 PR 描述：
## Summary     —— 改了什么、为什么（2–3 条）
## Test Plan    —— 如何验证这些改动
保持简洁。
```

> ⭐ "Summary 讲 why，Test Plan 讲 how to verify"——
> 这个结构比"列出改了哪些文件"有用得多。

---

## 5. 调试助手

```
当我给出一个错误时：
1. 读完整堆栈跟踪
2. ⭐ 定位根因（不是症状）
3. 检查相关源文件
4. 提出带代码的修复
5. 解释为什么会出错

⭐ Don't guess — read the actual code first.
```

详尽版见（已移至 _parked 领域实例库）的 `systematic-debugging-skill.md`。

---

## 6. 测试生成器

```
为当前文件生成测试，覆盖：
- Happy path
- Edge cases（空输入、null、边界）
- Error cases
- Integration points

⭐ 使用项目现有的测试框架和模式
⭐ 匹配仓库里已有测试的风格
```

> ⭐ 后两条是它比"写点测试"有效的原因——
> 与 `testing-skills.md` 的"框架检测 + 模式匹配"一致。

---

## 7. 文档生成器

```
为指定的函数/类/模块：
1. 写清晰的 docstring
2. 带类型地文档化参数
3. 文档化返回值
4. 加用法示例
5. 注明副作用或异常

⭐ 遵循项目现有的文档风格
```

---

## 8. 五条实战提示

| 提示 | 说明 |
|---|---|
| ⭐ **要具体** | "审查安全问题" 优于 "审查代码" |
| **给示例** | 展示你想要的输出格式 |
| ⭐ **设约束** | "最多 5 个问题" 能防止噪音 |
| **引用工具** | "用 git diff" 告诉 Claude 该读什么 |
| **迭代** | ⭐ 先简单起步，随着你学到什么管用再补细节 |

> 第 3 条特别值得抄：
> **不加数量上限的审查技能，会输出 30 条发现，其中 25 条是噪音。**

---

## 速查

| 技能 | 核心约束 |
|---|---|
| 代码审查 | ⭐ Skip praise；只报真问题 |
| commit | Conventional Commits，首行 ≤72 字符 |
| PR 描述 | Summary(why) + Test Plan(how) |
| 调试 | ⭐ 先读代码再猜 |
| 测试生成 | ⭐ 匹配现有框架与风格 |
| 文档生成 | ⭐ 遵循项目现有风格 |
