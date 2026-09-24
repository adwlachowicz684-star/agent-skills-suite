# reference 文件的组织与加载

> 相关：《skill-structuring》的 `directory-decision-matrix.md` ·
> `references-vs-assets.md` · 《skill-patterns》的
> `progressive-disclosure-official.md` · `reference-organization.md`
> 前置：那些文档讲"要不要放进 references"，这份讲⭐ 放进去之后怎么组织。

---

## 目录

- [1. ⭐ 加载时机：三个阶段](#1--加载时机三个阶段)
- [2. ⭐⭐ 保持一层深度](#2--保持一层深度)
- [3. ⭐ 超 100 行要带目录](#3--超-100-行要带目录)
- [4. 文件该怎么切](#4-文件该怎么切)
- [5. ⭐ 内联 vs 块引用](#5--内联-vs-块引用)
- [6. ⭐ 会被重复读取](#6--会被重复读取)

---

## 1. ⭐ 加载时机：三个阶段

```
发现阶段   只读 SKILL.md 的 frontmatter（name + description）
激活       ️ 加载 SKILL.md 全文
需要时     才加载**特定**的 reference 文件
```

> ⭐ 这意味着：**你可以有很多 reference 文件，
> 在真正被需要之前，它们完全不影响性能。**

---

## 2. ⭐⭐ 保持一层深度

> ⭐⭐ **避免深度嵌套的引用。**

**为什么**（这个机制解释很关键）：

```
⭐ 当引用来自"另一个被引用文件"时，模型可能只部分读取。
⭐ 遇到嵌套引用，它可能用 head -100 之类的命令预览，
   而不是读完整文件 → ⭐ 信息不完整。
```

```
❌ 太深：SKILL.md → a.md → b.md
✅ 一层：SKILL.md → a.md
        SKILL.md → b.md
```

> ⭐ 与 `progressive-disclosure-official.md` 的结论完全一致：
> **所有 reference 文件都应从 SKILL.md 直接链接。**

---

## 3. ⭐ 超 100 行要带目录

```
⭐ 超过 100 行的 reference 文件，顶部要有目录（TOC）。
```

**为什么**：

```
⭐ 确保模型即使用部分读取（预览）的方式，
⭐ 也能看到可用信息的完整范围。
```

> ⭐ 这是对上面"会被部分读取"这一事实的**主动适配**——
> 既然知道它可能只看开头，就把地图放在开头。

---

## 4. 文件该怎么切

**按主题切，不按"什么时候用"切**：

```
✅ references/
     authentication.md   （只讲认证）
     error-handling.md   （只讲错误处理）
     pagination.md       （只讲分页）

❌ references/
     advanced.md         （"高级"不是主题）
     part2.md            （编号不是内容）
     everything.md       （2000 行混合内容）
```

**命名规则**：

```
⭐ 文件按内容命名，不按使用时机命名
✅ react-hooks.md · typescript-types.md
❌ advanced.md · part2.md
```

**体量**：

```
⭐ 每个文件控制在 200 行以内
⭐ 超了就按子主题再切
```

**每个文件开头要有上下文说明**：

```markdown
# React Hooks Patterns

This reference covers common React hooks patterns for this skill.
Parent skill: component-generator
```

> ⭐ "Parent skill" 那行很有用：**文件被单独读到时，
> 模型仍知道它属于哪个技能、服务于什么。**

**复杂技能用层级目录 + 索引**：

```
api-skill/
├── SKILL.md
└── references/
    ├── rest/      conventions.md · error-codes.md · versioning.md
    ├── graphql/   schema.md · resolvers.md
    ├── common/    authentication.md · rate-limiting.md
    └── index.md   ⭐ 大集合要加索引
```

---

## 5. ⭐ 内联 vs 块引用

两种方式会让模型有不同行为：

**内联（加载并采纳）**：

```
See `references/examples.md` for examples of this pattern.
```

**块引用（显式指令）**：

```
## Extended Examples
Before proceeding, read the full examples in `references/examples.md`
and apply those patterns to the current task.
```

> ⭐ 差别在于强制程度。需要确保必读时用"块引用"措辞
> （"Before proceeding, read..."）。

---

## 6. ⭐ 会被重复读取

> ⭐ **每次模型遇到 "see references/X.md" 这样的指令，它就会读一次该文件。**
> ⭐ **内容不会在轮次之间持久保留**（除非它正在显式地用这些内容）。

**应对**：

```
⭐ 对高频需要的 reference 数据：
   在 SKILL.md 里放一份精简摘要，
   完整文件只在边界情形才引用。
```

> ⭐ 这条容易被忽略：你以为"引用一次就记住了"，
> 实际上每轮都可能重读，重复付 token。

**验证的方法**：

```
⭐ 测试模型是否真的在需要时读取了你的 reference。
   没有的话，就把引用写得更显式一些。
```

---

## 速查

```
□ ⭐⭐ 引用只保持一层深度（嵌套会被 head -100 截断）
□ ⭐ 超 100 行的文件顶部带目录
□ ⭐ 按主题切分，不按"高级/part2"切
□ ⭐ 按内容命名，不按使用时机命名
□ 单文件 ≤200 行
□ ⭐ 每个文件开头写明 Parent skill
□ 大集合用子目录 + index.md
□ ⭐ 需要确保必读时用块引用措辞（"Before proceeding, read..."）
□ ⭐⭐ 同一 reference 可能每轮重读，高频数据要在正文放摘要
□ ⭐ 要实际验证模型确实读了（没读就把引用写得更显式）
□ 更新 SKILL.md 时同步检查 reference 是否需要更新
□ 起步阶段先只有 SKILL.md，长大了再加 reference（别过度设计）
```

**一句话**：

> ⭐⭐ **嵌套引用会让模型改用 `head -100` 预览——
> 所以要么保持一层，要么在文件顶部放一份目录。**
