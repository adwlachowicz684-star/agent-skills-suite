# 激活机制：为什么 description 是唯一的杠杆

> 相关：《skill-description》的 `activation-rate.md` ·
> `imperative-description.md` · `description-rewrite-case.md`

---

## 目录

- [1. ⭐ 纯 LLM 推理，不是检索](#1--纯-llm-推理不是检索)
- [2. 三步机制](#2-三步机制)
- [3. 推论](#3-推论)
- [4. ⭐ 与向量检索方案的关系](#4--与向量检索方案的关系)

---

## 1. ⭐ 纯 LLM 推理，不是检索

> ⭐ **Claude 用纯 LLM 推理来决定技能激活——
> 不是 embeddings、不是分类器、不是关键词匹配。**

这一条推翻了很多人的直觉，也解释了几个反常现象。

---

## 2. 三步机制

```
① 所有技能的 name + description 被注入系统提示词（每个约 100 tokens）
② 语言模型通过正常推理决定调用哪个技能
③ ⭐ 完整的 SKILL.md 内容只在激活决定之后才加载
```

---

## 3. 推论

既然是纯推理，那么：

```
✅ 有效：改变描述给模型的"理由"（祈使句、否定约束、触发同义词）
❌ 无效：keywords 字段（模型不看它做路由）
❌ 无效：单纯堆关键词（变体 B ≈ 变体 A）
❌ 有害：强制注入 hook（与技能意图冲突，最多降 30pp）
```

> ⭐ **`description` 是你控制激活的唯一杠杆。**

一个好用的判据：

```
坏描述读起来像营销文案
好描述读起来像工单的第一行
```

另一个实用技巧——**列出触发面的同义词**：

```yaml
description: Use when continuing work from a previous AI coding-agent session,
  handoff transcript, chat log, exported conversation, saved artifact set,
  or session summary.
```

> ⭐ 这样无论用户说"恢复我的会话"还是"从这个聊天记录接着来"，都能命中。

---

## 4. ⭐ 与向量检索方案的关系

`vector-skill-retrieval.md` 讲的是**在决策前用向量检索缩候选**。
但要注意：**平台内置的激活决策是纯 LLM 推理**。

所以：

```
平台内置    → 纯推理，只能靠 description
自建编排层  → 可以用向量检索 + Rerank 缩到 3–8
```

> ⭐ **两者不冲突，是不同层次**：
> 内置路由优化靠写 description；
> 当你自建了编排层（技能极多时），才上检索。

顺序依然是：**先写好 description、拆清职责，再考虑检索**。

---

## 速查

| 想提高激活率 | 手段 |
|---|---|
| 内置路由 | ⭐ 祈使句 + 否定约束 + 触发同义词 |
| 无效手段 | ❌ keywords 字段 / 堆关键词 / 强制 hook |
| 技能极多 | 自建编排层 + 向量检索 Top-K 3–8 |
| 描述风格 | ⭐ 像工单第一行，不像营销文案 |
