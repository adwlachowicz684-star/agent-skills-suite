# 官方渐进式披露三模式

> 相关：`skill-crafting` 的 `skill-structuring` 的 `reference-routing.md`（引用一层深）·
> `skill-structuring` 的 `references-vs-assets.md` · 《skill-refining》的 `splitting.md`

---

## 目录

- [1. 心智模型：像入职指南的目录](#1-心智模型像入职指南的目录)
- [2. 模式一：高层指南 + 参考引用](#2-模式一高层指南--参考引用)
- [3. ⭐ 模式二：按领域组织（多个域时必用）](#3--模式二按领域组织多个域时必用)
- [4. 模式三：条件式细节](#4-模式三条件式细节)
- [5. ⭐ 避免深层嵌套引用](#5--避免深层嵌套引用)
- [6. 长文件必须带目录](#6-长文件必须带目录)
- [7. 从简单到复杂的演进](#7-从简单到复杂的演进)

---

## 1. 心智模型：像入职指南的目录

> ⭐ **SKILL.md 是一份总览，需要时把 Claude 指向详细材料——
> 就像入职指南的目录。**

硬性约束：

```
⭐ 正文保持在 500 行以内以获得最佳性能
⭐ 接近这个上限时就把内容拆到独立文件
```

---

## 2. 模式一：高层指南 + 参考引用

```
pdf/
├── SKILL.md        主指令（触发时加载）
├── FORMS.md        表单填写指南（按需加载）
├── reference.md    API 参考（按需加载）
└── examples.md     用法示例（按需加载）
```

Claude 只在需要时加载 `FORMS.md` / `REFERENCE.md` / `EXAMPLES.md`。

**要点**：主文件要在正文里**明确写出"何时该去读哪份"**，
否则模型不知道该触发哪一次加载。

---

## 3. ⭐ 模式二：按领域组织（多个域时必用）

> ⭐ **当技能覆盖多个领域时，按领域组织内容，避免加载无关上下文。**

```
bigquery-skill/
├── SKILL.md            总览与导航
└── reference/
    ├── finance.md      收入、计费指标
    ├── sales.md        商机、管道
    ├── product.md      API 用法、功能
    └── marketing.md    活动、归因
```

> 用户问销售指标时，Claude **只需要读 sales 相关的 schema**，
> 不需要 finance 或 marketing 的数据。

**收益**：token 用量低、上下文聚焦。

> ⭐ 这是"按域拆分"最标准的形态，
> 与 `skill-structuring` 的 `references-vs-assets.md` 的"理解 vs 使用"判据互补：
> 先按域分，再判每份是 references 还是 assets。

一个写法示例——在主文件里给出**带路由提示的表**：

```markdown
| 域 | 文件 | 何时读 |
|---|---|---|
| 财务 | `reference/finance.md` | 提到收入、计费 |
| 销售 | `reference/sales.md` | 提到商机、管道 |
```

---

## 4. 模式三：条件式细节

```
展示基础内容，把高级内容链接出去
```

> Claude 只在用户需要那些特性时才读 `REDLINING.md` 或 `OOXML.md`。

写法：

```markdown
## 基础用法
（这里写默认路径）

## 高级
需要红线批注时，读 `REDLINING.md`。
需要直接操作 OOXML 时，读 `OOXML.md`。
```

---

## 5. ⭐ 避免深层嵌套引用

> ⭐ **Claude 从被引用文件里再遇到引用时，可能只做部分读取。**

具体表现：

```
遇到嵌套引用 → Claude 可能用 head -100 预览
             → ⭐ 而不是读完整文件
             → 结果信息不完整
```

**规则**：

```
✅ 引用文件直接从 SKILL.md 链接（一层深）
❌ SKILL.md → A.md → B.md（太深）
```

> ⭐ 所有参考文件都应**直接从 SKILL.md 链接**，
> 以确保 Claude 在需要时读到完整文件。

---

## 6. 长文件必须带目录

> ⭐ **超过 100 行的参考文件，在顶部放一个目录。**

原因正是上面那条：模型可能做部分读取。
有目录，它**即使只预览也能看到全貌**，
然后决定读全文还是跳到特定章节。

---

## 7. 从简单到复杂的演进

```
① 起步：只有一个 SKILL.md（元数据 + 指令）
② 长大：按需捆绑额外内容
③ 完整形态：SKILL.md + references/ + scripts/
```

```
pdf/
├── SKILL.md
├── FORMS.md
├── reference.md
├── examples.md
└── scripts/
    ├── analyze_form.py
    ├── fill_form.py
    └── validate.py
```

> ⭐ 注意 `scripts/` 里的是**被执行，不被加载**——
> 这是 `skill-structuring` 的 `references-vs-assets.md` 那条成本差异的第三种形态。

---

## 速查

| 情况 | 模式 |
|---|---|
| 单一域，内容多 | 模式一：主文件 + references |
| ⭐ 多个域 | ⭐ 模式二：按域拆分 + 路由表 |
| 有基础/高级之分 | 模式三：条件式 |
| 引用链 | ⭐ 只一层，都从 SKILL.md 出发 |
| 参考文件 >100 行 | ⭐ 顶部加目录 |
