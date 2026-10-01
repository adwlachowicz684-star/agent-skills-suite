---
name: skill-automation
description: 技能评测与运维的自动化执行：CI 门禁、评测工具链、A/B 自动跑、灰度与回滚、遥测与 span 日志。当需要把技能检查接入流水线、自动跑 A/B、做灰度发布、接入可观测性，或排查"CI 是绿的但技能还是坏了"时使用。
  Do NOT use for 该测什么、怎么判分（用 skill-evaluating / skill-quality）、触发不生效（用 skill-triggering）。
---

# 评测与运维自动化

## 边界

- 用于：**怎么自动跑、在哪跑、跑完怎么看**
- 不用于：测什么、怎么判分 → 《skill-evaluating》《skill-quality》
- 不用于：技能没被触发 → 《skill-triggering》
- 不用于：版本策略与影响面 → 《skill-versioning》

## 核心原则

> ⭐⭐⭐⭐⭐ **CI 是绿的，不代表技能是好的。**
> ⭐⭐⭐⭐⭐ Claude Code 是交互式工具，不是 CI runner——
> 你无法在流水线里调起它去测技能行为。

```
□ ⭐⭐⭐⭐⭐ CI 能验结构，不能验行为
□ ⭐⭐⭐⭐⭐ 配置引导着 agent，因此它值得拿到代码所享有的回归测试
□ ⭐⭐⭐⭐⭐ 每次生产事故产生一条 eval，永久留在套件里
□ ⭐⭐⭐⭐ 缓存命中率要像可用性一样监控
□ ⭐⭐⭐⭐⭐ 10% 流量全挂，大盘只掉 1–2 个点
```

## 路由表（按需深读）

| `skill-automation/references/ci-skill-validation.md` | ⭐⭐⭐⭐⭐ CI 能验什么、不能验什么；按名字强制 disable-model-invocation |
| `skill-automation/references/ci-gate-integration.md` | ⭐⭐⭐⭐ 门禁接入与失败分级 |
| `skill-automation/references/eval-tooling.md` | ⭐⭐⭐⭐ 评测工具链选型 |
| `skill-automation/references/claude-ab-loop.md` | ⭐⭐⭐⭐⭐ 用 `claude -p` 跑行为评测；四个设计 |
| `skill-automation/references/comparator-ab-eval.md` | ⭐⭐⭐⭐ 盲评 comparator + 五条统计纪律 |
| `skill-automation/references/canary-release.md` | ⭐⭐⭐⭐⭐ 灰度：版本级指标拆分；跳档事故 |
| `skill-automation/references/skill-observability.md` | ⭐⭐⭐⭐ 调用日志 vs 决策日志；入参记两份 |
| `skill-automation/references/execution-span-logging.md` | ⭐⭐⭐⭐⭐ `stopped_at`：从"要排查整个技能"缩小到"看一个步骤" |
| `skill-automation/references/production-drift-signals.md` | ⭐⭐⭐⭐⭐ 不跑 eval 的漂移检测：六个免费信号；⭐⭐⭐⭐⭐ 基线是它自己不是全库均值；⭐⭐⭐⭐⭐ 只看均值会漏掉"对但不稳" |
| `skill-automation/references/flaky-gate-discipline.md` | ⭐⭐⭐⭐⭐ 门禁失效的方式是**被忽略**不是变绿；同一 commit 跑 3 次；⭐⭐⭐⭐⭐ "重跑就绿了"在训练团队忽略红灯；quarantine 必须有时限 |
| `skill-automation/references/eval-scheduling-budget.md` | ⭐⭐⭐⭐⭐ 全量评测太慢 → 逐步缩成冒烟 → 绿灯仍在；三层调度；⭐⭐⭐⭐⭐ 重复次数最低 2 次（1 次是质变）；带债合入要有配额 |
| `skill-automation/references/automation-coverage-blindspot.md` | ⭐⭐⭐⭐⭐ 能力边界 vs **配置边界**（后者无人审视）；⭐⭐⭐⭐⭐ 差集检查：担心的 vs 检查的；"有 CI"≠"有覆盖" |
| `skill-automation/references/gate-bypass-threshold.md` | ⭐⭐⭐⭐⭐ 绕过路径在最没能力复核的时刻取消唯一一道复核；⭐⭐⭐⭐⭐ 调阈值是最容易的"修"；阈值 ≥1.0 = 已失效的保护 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 名字含 `deploy/commit/send/delete/migrate/push` → 强制 `disable-model-invocation: true`（可 grep 的机械检查）
- ⭐⭐⭐⭐⭐ 行为评测走 `claude -p`，不要指望 CI 里的结构检查
- ⭐⭐⭐⭐⭐ 灰度期必须做版本级指标拆分，大盘平均分掩盖全挂
- ⭐⭐⭐⭐ 失败全量记录、成功采样（失败样本信息量远高于成功样本）
- ⭐⭐⭐⭐⭐ 某步骤 `ok=false` 反复出现 → 那一步该进 Gotchas
- ⭐⭐⭐⭐⭐ 用例重复次数最低 2 次——1 次会让"不稳定"彻底不可见
- ⭐⭐⭐⭐⭐ 调阈值前先问：这是在修问题，还是在分期关闭告警
- ⭐⭐⭐⭐⭐ 阈值 ≥ 1.0 或白名单 > 10% = 已失效的保护（可 grep 的机械检查）

## 何时不用（边界）

- ⭐⭐⭐ "断言该怎么写" → 《skill-evaluating》的 `benchmark-assertions-delta`
- ⭐⭐⭐ "分数怎么解读" → 《skill-quality》
- ⭐⭐⭐ "改了之后影响谁" → 《skill-versioning》

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验（CI 第一道） |
| `scripts/estimate_tokens.py <dir>` | 成本估算 |

## 参考

- 相关技能：《skill-evaluating》（测什么）·《skill-quality》（怎么判）·
  《skill-versioning》（版本与回滚）·《skill-governance》（SLO 与成本）
