# frontmatter 字段：四个必需 + 六个元数据

> 相关：《skill-crafting》的 `skill-structuring` 的 `frontmatter-pitfalls.md` ·
> 《skill-refining》的 `version-strategy.md` ·
> `skill-structuring` 的 `directory-contract.md`

---

## 目录

- [1. 四个必需字段](#1-四个必需字段)
- [2. ⭐ 六个元数据字段](#2--六个元数据字段)
- [3. 六个必需章节](#3-六个必需章节)
- [4. ⭐ 每个步骤的 Expected / On failure](#4--每个步骤的-expected--on-failure)
- [5. ⭐ 四个常见漏检](#5--四个常见漏检)

---

## 1. 四个必需字段

```
name            ⭐ kebab-case，必须与目录名一致
description     ⭐ <1024 字符
license         许可证
allowed-tools   允许的工具
```

**name 的约束**：

```
⭐ 仅小写字母、数字、连字符，最长 64 字符
⭐ 必须与目录名匹配
⭐ name 是标识符；# 标题是人类可读的，可以不同
   例：name: review-skill-format，标题 # Review Skill Format
```

---

## 2. ⭐ 六个元数据字段

```
author       作者
version      版本（语义化，"1.2.3" 推荐但不强制）
domain       所属领域
complexity   复杂度（basic / intermediate / advanced）
language     语言（multi 表示多语言）
tags         标签（列表）
```

**注册表示例**：

```yaml
- id: skill-name
  path: skill-name/SKILL.md
  complexity: intermediate
  language: multi
  description: One-line description
```

> ⭐ **`complexity` 在范围扩大时要更新**（如 basic → intermediate）；
> **`tags` 在覆盖领域变化时要更新**；
> ⭐ **`description` 在技能范围实质变化时要更新**。

**扩展字段是安全的**：

> ⭐ **如果 agent 遇到它不理解的字段，会忽略——
> 所以你可以加扩展字段而不用担心破坏可移植性。**

可选的身份字段（另一套口径）：

```
created   创建日期（ISO 8601）
updated   最后更新日期
```

---

## 3. 六个必需章节

```
① When to Use
② Inputs
③ Procedure
④ Validation
⑤ Common Pitfalls
⑥ Related Skills
```

> ⭐ **Validation 章节有两种写法都算通过**：
> `## Validation` 或 `## Validation Checklist`——
> **检查时两种标题都要认**。

---

## 4. ⭐ 每个步骤的 Expected / On failure

> ⭐ **每个流程步骤都必须有 `Expected:` 和 `On failure:` 块。**

```markdown
### Step 3: Run migration
Expected: 迁移成功，schema 版本号 +1
On failure: 回滚到上一版本并报告阻塞原因
```

为什么这条重要：

```
① ⭐ 编号或清单化结构让失败点可被定位——
   审计说"第 3 步坏了"，作者知道是哪里
② ⭐ 有输入→输出契约，下游技能才能对着已知形状组合
③ ⭐ 没有 On failure，agent 遇到异常就自己瞎编
```

对照组：

```
✅ Step 1 加载 reference · Step 2 综合 · Step 3 写入 docs/.../YYYY-MM-DD-*.md
❌ "你大概应该看一下 references，然后考虑写点什么"
```

> ⭐ 后者的问题不只是含糊（"应该"、"考虑"），
> **而是没有可定位的失败点**。

---

## 5. ⭐ 四个常见漏检

```
① ⭐ 只用正则检查 frontmatter
   ⭐ YAML 解析很微妙：
      description: >    （多行块）
      description: "inline"
      看起来不一样——搜字段时两种模式都要检查

② ⭐ 漏掉 Validation 章节的变体（见上）

③ ⭐ 忘记更新注册表总数
   ⭐ 加技能到注册表后，顶部的 total_skills 也必须递增
   ⭐ 这是 PR 里最常见的疏漏

④ ⭐ 宽松模式下跳过了阻塞项
   ⭐ 宽松模式只放宽风格和元数据建议，
      ⭐ 缺失必需章节和 frontmatter 字段仍必须报告
```

**翻译技能的额外检查**：

```
· 五个翻译字段：locale / source_locale / source_commit / translator / translation_date
· ⭐ 正文段落必须是目标语言，不是英语
    （非英语 frontmatter + 非英语标题 + 英语正文，能通过所有结构检查
     ——⭐ 所以必须单独验证正文语言）
· 代码块与英文源保持一致
```

---

## 速查

```
必需四字段：
□ name（kebab-case，与目录名一致）
□ description（<1024）
□ license
□ allowed-tools

元数据六字段：
□ author / version / domain / complexity / language / tags

六章节：
□ When to Use · Inputs · Procedure · Validation · Common Pitfalls · Related Skills

☐ ⭐ 每步有 Expected: 和 On failure:
□ ⭐ 行数 ≤500
□ ⭐ 注册表里 total_skills 准确
□ ⭐ 正则检查要覆盖 > 和 "inline" 两种写法
□ ⭐ 宽松模式也不能放过必需项
□ 扩展字段安全（未知字段被忽略）
□ 翻译技能要单独验正文语言
```

**一句话**：

> ⭐ **编号结构让失败点可被定位——
> 审计说"第 3 步坏了"，你得知道那是哪里。**
