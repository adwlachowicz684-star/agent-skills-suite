---
name: skill-examples
description: 技能里的示例与判断依据：示例从轨迹采集而非编写、示例值会被当成默认值、少示例的质量准则、示例的三分支覆盖、判断分支与验收条件、决策依据必须可查而非可编。当技能要加示例、示例效果不好、输出看起来合理但不可复现、或要判断"这段该给示例还是给规则"时使用。
  Do NOT use for 措辞与文体（用 skill-crafting）、输出格式与长度（用 skill-output）、正文瘦身（用 skill-refining）。
---

# 示例与判断依据

## 边界

- 用于：**示例怎么来、怎么放、放几个、以及判断依据怎么写**
- 不用于：措辞、文体、含糊词 → 《skill-crafting》
- 不用于：输出模板与长度 → 《skill-output》
- 不用于：正文删减 → 《skill-refining》

## 核心原则

> ⭐⭐⭐⭐⭐ **示例有两种，混着写就都失效：
> 定格式的该编（干净、规范），教判断的必须采集（带杂讯、带 Rationale）。**
> ⭐⭐⭐⭐⭐ **你没法阻止模型复制示例的值，那就让它复制到会暴露自己的东西。**

```
□ ⭐⭐⭐⭐⭐ 如果示例读起来像教科书，说明你编了
□ ⭐⭐⭐⭐⭐ 少样本示例是最强的上下文信号——信任度高于指令
□ ⭐⭐⭐⭐⭐ 判断依据必须可查，解释是可以编的
□ ⭐⭐⭐⭐⭐ 示例要带 Rationale，否则模型学到的是格式不是判断
□ ⭐⭐⭐⭐ 三个示例覆盖三个分支，不是同一个分支的三个版本
□ ⭐⭐⭐⭐ 少了验收，agent 会用一句"已完成"糊过去
```

## 路由表（按需深读）

| `skill-examples/references/example-overrides-instruction.md` | ⭐⭐⭐⭐⭐ 示例与正文冲突时模型跟示例；⭐⭐⭐⭐⭐ 示例是唯一看起来不是指令的指令；改正文必须同步示例 |
| `skill-examples/references/example-values-become-defaults.md` | ⭐⭐⭐⭐⭐ 示例值被当成默认值；换成会暴露自己的假值 |
| `skill-examples/references/example-mining-from-traces.md` | ⭐⭐⭐⭐⭐ 示例是采集的；六个矿脉；被采纳的输出才是好示例 |
| `skill-examples/references/few-shot-example-quality.md` | ⭐⭐⭐⭐⭐ 少示例的数量与质量准则；模糊输入示例 |
| `skill-examples/references/examples-three-branches.md` | ⭐⭐⭐⭐⭐ 三分支覆盖 + Rationale 字段 |
| `skill-examples/references/few-shot-examples.md` | ⭐⭐⭐⭐ 少示例总纲 |
| `skill-examples/references/judgment-branches-acceptance.md` | ⭐⭐⭐⭐⭐ 流程/判断/验收三件套；差评反例 |
| `skill-examples/references/decision-rationale-output.md` | ⭐⭐⭐⭐⭐ 因为更好不是依据，因为规则3b才是 |
| `skill-examples/references/example-placement-and-rot.md` | ⭐⭐⭐⭐⭐ 示例占比＞1/3 会稀释正文；⭐⭐⭐⭐⭐ 示例比正文烂得快（具体标识符）；⭐⭐⭐⭐⭐ 腐烂可 grep |
| `skill-examples/references/example-order-recency.md` | ⭐⭐⭐⭐⭐ 最后一条示例权重最高；⭐⭐⭐⭐⭐ 而它通常是最晚随手加的；反例不能放最后 |
| `skill-examples/references/negative-example-writing.md` | ⭐⭐⭐⭐⭐ 模型从反例学到的是字面形式不是规则；最小差异对；⭐⭐⭐⭐⭐ 反例必须带正面对应物 |
| `skill-examples/references/example-contract-consistency.md` | ⭐⭐⭐⭐⭐ 拿 schema 校验自己的示例；⭐⭐⭐⭐⭐ schema 在校验示例的复制品；示例赢契约 |
| `skill-examples/references/example-shapes-trigger-boundary.md` | ⭐⭐⭐⭐⭐ 示例输入侧隐式定义触发边界；方差为零的维度被当成常量；输入形态说明约 20 token |

## Critical Rules

- ⭐⭐⭐⭐⭐ 格式示范用假值（`2099-01-01`、`¥1`），判断依据用真值
- ⭐⭐⭐⭐⭐ 定格式的示例可以编，教判断的示例必须来自真实轨迹
- ⭐⭐⭐⭐⭐ 每个示例必须说明"为什么在这个场景该这么处理"
- ⭐⭐⭐⭐⭐ 最后一条示例权重最高——它必须是精心挑选的，不能是随手追加的
- ⭐⭐⭐⭐⭐ 拿 schema 校验自己的每个示例；schema 报错时先校验示例
- ⭐⭐⭐⭐⭐ 示例的输入侧要有方差：方差为零的维度会被当成常量
- ⭐⭐⭐⭐ 示例集必须包含一个"模糊输入"的示例（其余教流程，只有它教判断）
- ⭐⭐⭐⭐ 正文里的负例要 sparingly（测评集的负例要充分）
- ⭐⭐⭐⭐⭐ 决策依据必须指向具体输入和规则，不能是"更好""更简洁"

## 何时不用（边界）

- ⭐⭐⭐ "这个词该不该用" → 《skill-crafting》的 `vague-word-blacklist`
- ⭐⭐⭐ "输出该多长" → 《skill-output》的 `output-length-budget`
- ⭐⭐⭐ "要不要删掉这段" → 《skill-refining》的 `pruning`

## 参考

- 相关技能：《skill-crafting》（措辞）·《skill-content》（Gotchas 采集）·
  《skill-output》（输出契约）·《skill-evaluating》（评测集）
