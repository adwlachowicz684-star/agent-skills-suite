---
name: skill-evaluating
description: 评估一个 Agent Skill 到底有没有用。用于技能不触发 / 乱触发 / 改了不生效 / 触发后跑偏、要做 A/B 配对对照、算 Skill Lift、跑四层测试金字塔、做质量评分 Rubric、排查加载失败与运行时问题。
  Do NOT use for 从零写技能（用 skill-authoring）、瘦身拆分（用 skill-refining）、安全审计与合规（用 skill-governance）、打包发布（用 skill-distribution），也不用于单纯解释概念。
---

# 评估技能有没有用

## 边界

- 用于：**触发测试** · **配对对照** · **质量评分** · **排错** · **运行时诊断**
- 不用于：从零写 · 瘦身拆分 · 安全审计 · 打包发布

## 核心原则

> ⭐ **唯一有意义的问题**：
> **"有这个技能" 比 "没有这个技能" 好多少？**

```
基线对照（必须做）
  同一任务跑两遍：启用技能 / 不启用技能
  ⭐ 回归量常常大到主导排序
  ⭐ 两组要跑在各自独立环境里
```

> ⭐ **NVIDIA 实测 300+ 技能**：正确性 46→87（+41）、可发现性 +40、有效性 +39、效率 +35。
> ⭐ **但代价是 token +120.3%、耗时 34s→41.1s**——提升与代价必须一起看。

## 路由表（按需深读）
| `priority-override-layers.md` | ⭐⭐⭐ 临时Prompt>技能>全局Rule；用非作者措辞测试 |
| `quality-rubric-nine-dims.md` | ⭐ 九维权重：实测表现 23 最高；这把尺子量不到什么 |
| `frontmatter-advanced-fields.md` | ⭐ fork/agent/hooks + 调用控制三档 |
| `skill-test-pyramid-four.md` | ⭐⭐ L1结构→L4回归四层；先手跑再加CI |
| `frontmatter-full-reference.md` | ⭐ 全字段四组 + 开放标准 vs CC 扩展边界 |
| `skillsbench-vs-realworld.md` | ⭐⭐ 34,198 真实技能：优势从 20pp 压缩到 3pp，瓶颈在检索 |
| `incremental-debug-procedure.md` | ⭐ 最小配置起步、增量验证、diff 测试 |
| `skill-observability.md` | ⭐ 调用日志 vs 决策日志、入参记两份、评估≠监控 |
| `comparator-ab-eval.md` | ⭐ 盲评 comparator + 五条统计纪律 |
| `three-failure-modes.md` | ⭐ 欠触发/误触发/执行失败三类根因 + 15 条评测集 |
| `trace-debugging.md` | ⭐ 读 trace：找第一个错的 turn + 循环唯一根因 |
| `fault-injection-eval.md` | ⭐ 故障注入评测：先写恢复契约 + 故障矩阵 + 四判定 |
| `ci-gate-integration.md` | ⭐ CI 门禁：增量触发、P0/P1 分级、幂等 |
| `determinism-boundary.md` | ⭐ 确定性边界：什么必须放 Hook，什么放技能 |
| `description-by-collision-risk.md` | ⭐ description 按碰撞风险分级 + 混淆伙伴审计 |
| `assert-on-environment.md` | ⭐ 断言打在环境状态上 + pass^5 + 20 条路由集 |
| `eval-loop-official.md` | ⭐ 官方评估四步、benchmark delta、盲评 A/B |
| `capability-vs-preference.md` | ⭐ 能力型 vs 偏好型：评估方式完全不同 |
| `deterministic-first.md` | ⭐ 确定性优先：能用代码判的别交给模型 |
| `graded-rubric.md` | ⭐ 不要用全有或全无的 rubric：每维独立 0–1 |
| `eval-case-sources.md` | ⭐ 每次手动修复都变成一条用例；10–20 条就够 |

**先排除假故障**：

| 症状 | 读 |
|---|---|
| ⭐ **改了不生效 / 技能不加载** | `references/reload-debug.md` |
| **四层定位法 / 症状诊断表** | `references/troubleshooting-manual.md` |
| **触发不稳：欠触发 / 过触发 / 冲突** | `references/triggering.md` · `references/trigger-debugging.md` |

**正式评估**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **四层测试金字塔（lint/触发/行为/回归）** | `references/test-pyramid.md` |
| ⭐ **Skill Lift：A/B 对照方法** | `references/skill-lift-eval.md` |
| **评测工具、pass@k、能力 vs 回归** | `references/eval-tooling.md` |
| ⭐ **四维评估：Outcome/Process/Style/Efficiency 可代码化** | `references/four-dimension-eval.md` |
| ⭐ **LLM-as-Judge：四种形式、机器可读判据、偏差与校准** | `references/judge-design.md` |
| **官方有效性清单（逐项对照）** | `references/official-checklist.md` |
| ⭐ **金丝雀发布：把技能改动当可执行配置** | `references/canary-release.md` |
| ⭐ **触发 Eval 集：near-miss 负例是承重的一半** | `references/trigger-eval-set.md` |
| ⭐ **先手动跑一遍：eval 素材从哪来、--json 判分** | `references/manual-first.md` |
| ⭐ **套件维护：100% 通过是坏消息、三个版本号** | `references/suite-maintenance.md` |
| **八层质量模型、20 条起始用例** | `references/metrics.md` |
| ⭐ **回归基线套件：三跑、分类统计、防转移** | `references/regression-baseline.md` |
| ⭐ **质量评分 Rubric（Accuracy 有否决权）** | `references/quality-rubric.md` |
| **双实例迭代：A 写 B 测** | `references/claude-ab-loop.md` |
| ⭐ **三个评估角色 / 对抗测试 / 防过拟合** | `references/eval-roles.md` |
| **发现性测试** | `references/discovery.md` |

**理解失败**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **技能为什么会让人变差** | `references/failure-modes.md` |
| **测试方法论** | `references/testing.md` |

## 强制工作流（MANDATORY）

1. **问清"好"的定义**：正确性？省时间？格式稳定？——不同目标用不同指标。
2. **跑基线**：`python scripts/validate_skill.py <路径>`。
3. ⭐ **确认真的加载了**：让模型复述技能流程，对得上才算数（`reload-debug.md`）。
4. **分离触发测试与输出测试**：先测"该不该触发"，再测"触发后做对没有"。
5. ⭐ **配对对照**：同一任务跑「有/无技能」两遍，**跑 3 次取趋势**（单次不作数）。
6. **量成本**：token 与耗时——**技能不一定更省**。
7. **出判决**：给出分数与"是否值得保留"的明确结论。

## Critical Rules

- ⭐ **跑一次不算证据**——85% 的公开评测只跑 1 次，无置信区间；你要跑多次
- ⭐ **跨产品的差异（+2～+46）远大于跨框架的差异（~5）**——别用别人的平均分推断自己
- 负例优先级**高于**正例——不该触发时能不触发，比该触发时能触发更难也更重要
- ⭐ **"手动测试用自己的措辞"是最大的测试错误**——请同事用他的原话测
- **Accuracy 是唯一有否决权的维度**——漂亮的危险建议比丑陋的安全建议更糟
- 评分必须**引用具体证据**，否则会分数通胀
- 失败原因要能归因到具体层（结构/触发/行为/回归），混着测等于两眼一抹黑

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "跑一次通过了就算好" | 单次不作数。要跑多次看波动。 |
| "我用自己写的措辞测过，能触发" | ⭐ 那是作者的词汇不是用户的。请同事用他的说法测。 |
| "别人测出平均 +31 分" | 跨产品差异远大于平均分所能反映的。自己测。 |
| "技能让 token 涨了 120%，但效果好" | 可以接受——但必须把代价写进判决，不能只报提升。 |
| "加载失败我改了三遍了" | ⭐ 重启往往没用——先 `/reload-skills`，再查文件层。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 第 1 层：结构 lint
python scripts/gen_eval_set.py "技能用途一句话"   # 生成触发测试集
python scripts/estimate_tokens.py ./my-skill     # 量成本
```
