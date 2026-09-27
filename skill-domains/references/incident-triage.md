# 实例：事故分诊 Runbook

> 一个值得逐句读的真实技能——**它很短，但每一句都是踩过坑的**。

## 目录

- [这个技能长什么样](#这个技能长什么样)
- [为什么它好](#为什么它好)
- [可迁移的四条写法](#可迁移的四条写法)
- [对照：你的 runbook 大概率缺什么](#对照你的-runbook-大概率缺什么)

## 这个技能长什么样

```yaml
name: incident-triage-runbook
description: >
  The SRE team's runbook for triaging production latency and
  error-rate incidents. Use this whenever investigating an incident,
  a latency spike, elevated error rates, or when asked
  "what caused X" about a production service.
```

正文（结构）：

```
# Incident triage
If you change the order below, say why in #sre.     ← ⭐ 见下

## Order of operations
1. Pull deploys for the last 6h. Don't open the log first.
2. Line the deploy timestamps up against p99_latency_ms /
   error_rate for the paged service.
   State the gap ("deploy 14:31, p99 moves 14:33").
3. If a deploy lines up: pull the diff, read it.
   Check for the stuff in the next section.
4. Then grep the log to confirm. Don't grep to fish.
5. No deploy lines up → check db_pool_utilization across
   checkout/cart/auth/inventory, then upstream deps.

## Things that have burned us
In rough order of how often:
- per-row query where there used to be a batch
- cache decorator removed "temporarily"
- new query, no index
- blocking call in an async handler
- retry loop with no backoff

## Write-up
One line at the bottom:
> **Root cause:** <sha> — one sentence on the mechanism.
If it wasn't a deploy, put the component or upstream dep
where the sha goes (db-primary, stripe-api, whatever).
Still one sentence.
Everything above that line is evidence.
Keep it short; the long version goes in the postmortem doc.
```

## 为什么它好

**① description 含引号里的原话**

```
⭐ "what caused X"
```

直接把用户的**原话**写进触发条件。这是 `description-patterns.md`
里"匹配用户词汇"的教科书示范——
不是"根因分析"，而是人会真的打出来的那句话。

**② 每一步都带"不要怎样"**

```
⭐ "Don't open the log first."
⭐ "Don't grep to fish."
```

两条禁令都在**防止最自然的错误动作**：
人会本能地先去翻日志。技能明确禁止了它。
（注意：这是**禁令+配方**组合——先给了正确顺序，
禁令只是防止跑偏，符合 `guidance-forms.md` 的形态匹配。）

**③ "Things that have burned us"**

> ⭐ **这就是 Gotchas 章节，而且是带排序的 Gotchas**。

```
"In rough order of how often"     ← ⭐ 按频率排序，不是随意列举
```

五条全是**具体到可以直接对照检查**的模式：
逐行查询取代了批量、缓存装饰器被"临时"移除、新查询没索引……
**没有一条是"注意性能"这种正确的废话。**

**④ 输出契约逆向定义**

```
⭐ "Everything above that line is evidence."
```

先规定**最后一行是什么**，再规定**它上面全是证据**。
这是 `output-contract.md` 里 Schema-First 的一个极简版本——
**一行就能定义整个文档的结构**。

而且给了降级路径：

```
不是 deploy 导致的 → sha 的位置换成组件名或上游依赖
                     ⭐ 仍然是一句话
```

**⑤ "If you change the order below, say why in #sre"**

一句看似随意的话做了两件事：

```
① ⭐ 保护了步骤顺序（这是技能的核心资产）
② 把变更引导到一个可讨论的地方，而不是静默修改
```

## 可迁移的四条写法

**① 触发词用引号里的原话**

```yaml
description: ... or when asked "what caused X" about ...
```

**② 禁令写成"先别做 X"，而不是"要做 Y"**

```
✅ "Don't open the log first."
❌ "应该先查部署记录"   ← 也对，但弱得多
```

原因：禁令针对的是**最可能发生的错误动作**，
比正面指令更能防止跑偏。

**③ Gotchas 按频率排序**

```
"In rough order of how often"
```

> 排序本身就是信息——它告诉 agent **先查哪个**。

**④ 输出用"某一行是什么"来锚定**

```
⭐ "最后一行是 Root cause，它上面全是证据"
```

比"报告要简洁"有效得多，因为**它定义了文档的形状**。

## 对照：你的 runbook 大概率缺什么

拿这份对照自己的运维/分诊类技能：

```
□ ⭐ 有没有"先别做 X"？
     多数 runbook 只写"第一步查什么"，
     不写"千万别先翻日志"

□ ⭐ 有没有 Gotchas，而且是排序的？
     多数只写流程，不写"最容易踩的五个坑"

□ ⭐ 输出契约是不是只用一行就定义清楚了？
     多数写"报告要详细"，结果结构每次都不一样

□ 有没有处理"主线假设不成立"的分支？
     ⭐ 这份有：第 5 步就是"deploy 对不上时怎么办"
     多数 runbook 只有 happy path

□ ⭐ 有没有保护步骤顺序的机制？
     "改顺序要在 #sre 说明原因"
```

最后一条最容易被忽略，但它恰恰说明：
**这份技能的所有者知道，步骤顺序是这个技能最有价值的部分。**

## 一条提醒

这个技能**很短**（全文不到 40 行）。
它的价值不在篇幅，在于**每一行都是不可删的**。

> 用 `pruning.md` 的 no-op 测试逐行过一遍：
> 你会发现几乎删不掉任何一句——**这正是好技能的判据**。
