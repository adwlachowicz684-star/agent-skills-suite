# 描述要"稍微强势一点"

> 相关：《skill-description》的 `activation-rate.md` ·
> `imperative-description.md` · `description-rewrite-case.md` ·
> `activation-mechanism.md`

---

## 目录

- [1. ⭐ 官方原话](#1--官方原话)
- [2. 对照例子](#2-对照例子)
- [3. 为什么需要"强势"](#3-为什么需要强势)
- [4. 边界：强势不等于夸张](#4-边界强势不等于夸张)
- [5. 完整写法建议](#5-完整写法建议)

---

## 1. ⭐ 官方原话

> ⭐ **Anthropic 自己的指引说：把描述写得"a little bit pushy"（稍微强势一点），
> 因为 Claude 倾向于在技能本该有用时不去用它。**

这是一条很少被引用但很关键的官方建议。

---

## 2. 对照例子

```
✅ "Reviews staged git changes for security, logic, and style issues before commit"
   → 触发更可靠

❌ "Helps with code review"
   → 触发较弱
```

差别在于：前者说清了**具体做什么、对什么、在什么时机**；
后者是一个含糊的善意声明。

---

## 3. 为什么需要"强势"

根因是 `activation-mechanism.md` 那条：

> 激活是**纯 LLM 推理**。模型有一条更简单的
> **"直接自己干"**的默认路径。

所以在描述上要主动给出**调用本技能的理由**：

```
① 领域标识        —— 我是这方面的专家
② ⭐ 祈使句        —— ALWAYS invoke
③ 触发同义词列表  —— 覆盖各种说法
④ ⭐ 否定约束      —— 堵住直接执行的近路
```

四条合起来就是"强势"的具体含义——**不是语气强烈，而是信息完整且排他**。

---

## 4. 边界：强势不等于夸张

```
✅ 强势：具体、排他、带触发条件
❌ 夸张："强大""智能""最好用"——形容词没有路由价值
```

`description-rewrite-case.md` 的错误清单里，
"使用形容词如强大/智能/好用"被明确列为错误——
**它缺少实质性的动词和名词，模型无从匹配**。

> ⭐ 判据回到 `activation-mechanism.md` 那句：
> **坏描述读起来像营销文案，好描述读起来像工单的第一行。**

---

## 5. 完整写法建议

```yaml
description: >
  <领域> expert. ALWAYS invoke this skill when the user asks about
  <触发列表，含同义词与用户原话>. Do not <直接执行> directly —
  use this skill first.
```

配套检查：

```
□ 有具体动词与名词（不是形容词）
□ ⭐ 有 "ALWAYS invoke" 或等价的祈使表达
□ 列出了 3 个以上用户真会说的说法（含口语/错别字）
□ ⭐ 有否定约束堵住直接执行路径
□ 有边界说明（何时不该用）
□ 第三人称（不是 "I help you"）
□ 长度适中——⭐ 不超过 200 字
```

---

## 速查

| 要 | 不要 |
|---|---|
| ✅ 具体动词 + 名词 | ❌ "强大/智能" |
| ✅ ALWAYS invoke | ❌ "helps with" |
| ✅ 用户的原话 | ❌ 文档腔 |
| ✅ 否定约束 | ❌ 只说该做什么 |
| ✅ 像工单第一行 | ❌ 像营销文案 |
| ✅ ≤200 字 | ❌ 越长越好 |
