---
name: skill-governance
description: Agent Skills 的生命周期治理、库存与退役、腐烂检测、Owner 制度与变更流程、SLO 与错误预算、可观测性 Schema、成本控制与 CI/CD 门禁。用于建立技能库治理制度、决定退役与归档、设定质量指标与执法机制、控制成本。
  Do NOT use for 安全审计与注入防御、权限与沙箱设计、供应链风险（用 skill-security），也不用于单个技能的质量打分（用 skill-evaluating）。
  Do NOT use for 写技能内容（用 skill-authoring）、瘦身拆分（用 skill-refining）、质量与触发评估（用 skill-evaluating），也不用于一般性的代码安全审查。
---

# 安全、合规与治理

## 边界

- 用于：**安全审计** · **注入防御** · **沙箱** · **合规** · **遥测** · **CI 门禁** · **成本** · **生命周期**
- ⭐ **安全审计、注入防御、权限与沙箱、供应链 → 《skill-security》**
- 不用于：写技能内容 · 瘦身拆分 · 触发评估 · 一般性代码安全审查

## 核心原则

> ⭐⭐⭐⭐ **指标没有后果，就等于没有指标。**
> 它变成了"我们知道自己在变差"的记录，而不是阻止变差的机制。

| 你要做的事 | 读 |
|---|---|
| ⭐ **安全审计、注入防御、权限与沙箱、供应链** | **`skill-security`** |

```
□ ⭐ 恶意技能：SKILL.md 保持完全干净，恶意逻辑全在外部脚本里
   → ⭐ 只扫 SKILL.md 不够，必须扫 scripts/
□ ⭐ 反向 shell 类技能把安装指令藏在 "Prerequisites" 段落
   ——因为静态扫描器不解析自然语言文档
□ 2026-02 ClawHavoc 事件：2857 个技能里 341 个恶意（11.9%，后续升至 20%）
```

> ⭐ **扫描器的 SAFE 不等于安全**——先确认它实际启用了几个引擎。
> 真实例子：某工具号称四扫描器协同，干净机器上 **50% 能力离线**，
> 但**照样输出 "✅ SAFE"**——后台只剩 grep 正则在跑。

## 路由表（按需深读）
| `skill-governance/references/unowned-skills.md` | ⭐⭐⭐⭐ 无主技能：没人认领=没人修；Owner 是治理的最小可执行单元 |
| `skill-governance/references/skill-slo-error-budget.md` | ⭐⭐⭐⭐⭐ 有指标没执法；三条 SLI（触发准确/输出合格/⭐净增益）；错误预算三档状态 |
| `skill-governance/references/skill-decay-governance.md` | ⭐⭐⭐ 腐烂四症状 + 五条治理清单（review_after/无category拒绝注册） |
| `skill-governance/references/observability-trace-debug.md` | ⭐⭐ 用技能调试技能；护栏放包装脚本不放提示 |
| `skill-governance/references/deprecation-compat-strategy.md` | ⭐⭐ 跨版本循环依赖 + 废弃三阶段 + 可选参数优先 |
| `skill-governance/references/skill-ownership-changeflow.md` | ⭐ Owner 制度 + 变更七步 + 真实翻车案例 |
| `skill-governance/references/ops-iteration-sop.md` | ⭐ 运维四段式 + S/A/B 分级 + 五条红线 |
| `skill-governance/references/skill-min-record-card.md` | ⭐ 最小档案卡 9 字段 + Owner 责任线 + 六个触发点 |
| `skill-governance/references/retirement-pipeline.md` | ⭐ 退役四阶段（35-42天）+ 归档≠删除 + 降级诊断 |

**治理与观测**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **遥测 Schema：六类 Span、什么不该记** | `skill-governance/references/telemetry-schema.md` |
| **可观测性：怎么知道技能到底用没用** | `skill-governance/references/observability.md` |
| ⭐ **死技能检测：三类处置决策与四个判读陷阱** | `skill-governance/references/dead-skill-detection.md` |
| ⭐ **Langfuse vs LangSmith：数据驻留与成本** | `skill-governance/references/observability-tools.md` |
| ⭐ **调用控制：Skill(name) 权限语法与三种用法** | `skill-governance/references/skill-invocation-control.md` |

**流水线与成本**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **CI/CD 集成与失败闭环** | `skill-governance/references/ci-cd-integration.md` |
| **三个 token 桶、实测 8.5%、16x 案例** | `skill-governance/references/cost-control.md` |
| **提示缓存：中途加载是最贵的失效模式** | **`skill-selection` 的 `skill-selection/references/caching-economics.md`** |
| **运行时性能：冷启动预热、并行 IO** | **`skill-selection` 的 `skill-selection/references/performance.md`** |

**规模与生命周期**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **1,236 技能吃掉 36.6% 上下文** | `skill-governance/references/scale-effects.md` |
| ⭐ **技能清单与留存策略：治理的前提是知道有什么** | `skill-governance/references/skill-inventory.md` |
| **五阶段：草稿 → 活跃 → 成熟 → 废弃 → 归档** | `skill-governance/references/lifecycle.md` |
| **技能库运维与五维健康诊断** | **`skill-distribution` 的 `skill-distribution/references/library-ops.md`** |

## Critical Rules

- ⭐⭐⭐ **治理阶梯**：<10 只需描述质量 · 10–20 加触发评测 · 20–50 加腐烂治理 · >50 注册中心 + 路由编排
- ⭐⭐⭐⭐ 无 category 拒绝注册（准入门禁，不是建议）
- ⭐⭐⭐ `review_after` 到期自动审计——把"会不会过期"变成有日期的机制
- ⭐⭐⭐⭐ 退役四阶段 35–42 天；**归档 ≠ 删除**，归档超 6 个月确认不用才删
- ⭐⭐⭐⭐⭐ 没有恢复路径的空壳，就是没人承认的删除
- 一定要记 `top_k`——RAG 回归常常是它从 5 悄悄变成 20
- ⭐ **日志管道本身就会成为泄露源**——目标是"让 prompt 可 diff，但不可读"
- 部署者日志**留存 ≥6 个月**

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "没人用就删掉" | ⭐⭐⭐ 低频高价值的专家型技能最该留——留在库里、不装进项目。 |
| "归档了就是删了" | ⭐⭐⭐⭐ 归档可被恢复；删除不能。两者不同。 |
| "改个小描述不用走变更流程" | ⭐⭐⭐⭐ 70% 的线上事故来自"未经评估的微调"。 |
| "多记点日志方便排查" | 日志管道本身是泄露源。让 prompt 可 diff 但不可读。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 结构与路由校验
python scripts/estimate_tokens.py ./my-skill     # 量化上下文占用
```
