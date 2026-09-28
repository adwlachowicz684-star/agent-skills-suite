---
name: skill-context
description: 技能的上下文与 token 经济学：三级加载的预算、压缩与截断的边界、常驻成本与认知切换、成本归因与归账。当技能变多后变慢变贵、压缩后行为变了、要估算成本、或要决定"装多少算多"时使用。
  Do NOT use for 技能正文瘦身（用 skill-refining）、触发相关（用 skill-triggering）、输出长度（用 skill-output）。
---

# 上下文与预算

## 边界

- 用于：**上下文怎么分配、成本怎么算、压缩怎么影响行为**
- 不用于：正文怎么删 → 《skill-refining》
- 不用于：改长输出 → 《skill-output》的 `output-length-budget.md`
- 不用于：没触发 → 《skill-triggering》

## 核心原则

> ⭐⭐⭐⭐⭐ **认知切换是主要成本，不是常驻。**
> ⭐⭐⭐⭐⭐ **压缩带回的是"开头 5000"，不是"最重要的 5000"——
> 系统没有能力判断哪 5000 重要。**

```
□ ⭐⭐⭐⭐⭐ 开头是黄金位置，结尾次优，中间是黑洞
□ ⭐⭐⭐⭐⭐ 一个从没被触发过的技能，成本不是零
□ ⭐⭐⭐⭐⭐ 库存 100 个时，"考虑要不要用"比"真的用一次"还贵
□ ⭐⭐⭐⭐ 成本可见 ≠ 成本受控（预算未绑定决策点）
□ ⭐⭐⭐⭐⭐ 压缩是可订阅事件，关键约束可以重注入
□ ⭐⭐⭐⭐ 脚本源码不进上下文，脚本输出必进
```

## 路由表（按需深读）

| `context-budget-per-skill.md` | ⭐⭐⭐⭐⭐ 单技能预算三层；超预算先砍输出 |
| `skill-cost-attribution.md` | ⭐⭐⭐⭐⭐ 认知切换 $15–30/月 vs 常驻 $2–4；判断预算才是瓶颈 |
| `disclosure-math.md` | ⭐⭐⭐⭐⭐ 三级加载的精确数字；健康基线 8K = 窗口 4% |
| `context-compression.md` | ⭐⭐⭐⭐⭐ 压缩只保留前 5000；指令放顶部 |
| `context-engineering.md` | ⭐⭐⭐⭐ 上下文工程总纲 |
| `token-profiling.md` | ⭐⭐⭐⭐ 逐项测量而非总数 |
| `token-cost-optimization.md` | ⭐⭐⭐⭐ 伪技能陷阱与 Token 泄漏 |
| `budget-truncation.md` | ⭐⭐⭐⭐ 截断边界与被切掉的部分 |
| `context-budget.md` | ⭐⭐⭐ 预算分配 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 红线、失败处理、验收永不删除（省 100–300 token，代价是半天到几天排查）
- ⭐⭐⭐⭐⭐ 超预算第一选择永远是砍输出（零价值密度）
- ⭐⭐⭐⭐⭐ 同时挂载 ≤3 个技能（>3 成功率下滑）——这是质量上限，不是经济数字
- ⭐⭐⭐⭐ 关键规则在两端都写一遍（首因 + 近因效应）
- ⭐⭐⭐⭐ 缓存命中率要像可用性一样监控（allowed-tools 是缓存事件）

## 何时不用（边界）

- ⭐⭐⭐ "正文怎么精简" → 《skill-refining》的 `pruning` / `deduplication`
- ⭐⭐⭐ "输出该多长" → 《skill-output》的 `output-length-budget`
- ⭐⭐⭐ "改了不生效" → 《skill-loading》

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/estimate_tokens.py <dir>` | 成本估算 |

## 参考

- 相关技能：《skill-refining》（瘦身）·《skill-selection》（装多少）·
  《skill-loading》（加载机制）·《skill-output》（输出长度）
