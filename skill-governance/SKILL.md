---
name: skill-governance
description: Agent Skills 的安全审计、注入防御、合规治理、可观测性与生命周期管理。用于装第三方技能前的安全审查、防提示注入、沙箱隔离设计、企业合规与审计留痕、遥测 Schema 设计、CI/CD 门禁、成本控制、技能库规模化治理与退役。
  Do NOT use for 写技能内容（用 skill-authoring）、瘦身拆分（用 skill-refining）、质量与触发评估（用 skill-evaluating），也不用于一般性的代码安全审查。
---

# 安全、合规与治理

## 边界

- 用于：**安全审计** · **注入防御** · **沙箱** · **合规** · **遥测** · **CI 门禁** · **成本** · **生命周期**
- 不用于：写技能内容 · 瘦身拆分 · 触发评估 · 一般性代码安全审查

## 核心原则

> ⭐ **技能本身就是注入通道**——SKILL.md 会被自动加载进系统提示。

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
| `allowed-tools-least-privilege.md` | ⭐⭐ 最小权限四面红旗（bash+curl 危险组合） |
| `skill-ownership-changeflow.md` | ⭐ Owner 制度 + 变更七步 + 真实翻车案例 |
| `ops-iteration-sop.md` | ⭐ 运维四段式 + S/A/B 分级 + 五条红线 |
| `skill-min-record-card.md` | ⭐ 最小档案卡 9 字段 + Owner 责任线 + 六个触发点 |
| `retirement-pipeline.md` | ⭐ 退役四阶段（35-42天）+ 归档≠删除 + 降级诊断 |
| `injection-audit.md` | ⭐ 提示注入审计：六类红旗与徽章制 |

**安全**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **最小权限：访问控制其实mostly是工具设计** | `references/least-privilege.md` |
| ⭐ **供应链审计：四阶段 + 可复制的 grep 命令** | `references/supply-chain-audit.md` |
| ⭐ **Hook 风险：在推理前执行、exit 2 才阻止** | `references/hook-risk.md` |
| ⭐ **紧急停用：四层开关与多久能停** | `references/kill-switch.md` |
| **权限复核：为什么会膨胀、四个问题检查法** | `references/access-review.md` |
| ⭐ **技能市场对照与 ClawHub 2026-03 事件（386 个）** | `references/marketplace-security.md` |
| ⭐ **四类真实恶意技能、按 OWASP 逐类审计** | `references/security-audit-ops.md` |
| **风险评级、七域治理清单** | `references/security-review.md` |
| ⭐ **注入防御五层纵深、致命三件套** | `references/injection-defense.md` |
| **执行沙箱与隔离、按技能类型切片** | `references/sandbox-execution.md` |

**合规与观测**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **per-agent identity、6 个月留存、六项控制** | `references/compliance-audit.md` |
| ⭐ **遥测 Schema：六类 Span、什么不该记** | `references/telemetry-schema.md` |
| **可观测性：怎么知道技能到底用没用** | `references/observability.md` |
| ⭐ **死技能检测：三类处置决策与四个判读陷阱** | `references/dead-skill-detection.md` |
| ⭐ **Langfuse vs LangSmith：数据驻留与成本** | `references/observability-tools.md` |
| **可见性与调用控制、skillOverrides** | `references/runtime-controls.md` |
| ⭐ **调用控制：Skill(name) 权限语法与三种用法** | `references/skill-invocation-control.md` |

**流水线与成本**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **CI/CD 集成与失败闭环** | `references/ci-cd-integration.md` |
| **三个 token 桶、实测 8.5%、16x 案例** | `references/cost-control.md` |
| **提示缓存：中途加载是最贵的失效模式** | `references/caching-economics.md` |
| **运行时性能：冷启动预热、并行 IO** | `references/performance.md` |
| ⭐ **Agent 事故响应 Runbook** | `references/agent-incident-response.md` |
| ⭐ **PII 与敏感数据处理** | `references/pii-data-handling.md` |
| ⭐ **批准门：放哪一层、三种失效方式** | `references/approval-gates.md` |

**规模与生命周期**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **1,236 技能吃掉 36.6% 上下文** | `references/scale-effects.md` |
| ⭐ **技能清单与留存策略：治理的前提是知道有什么** | `references/skill-inventory.md` |
| **五阶段：草稿 → 活跃 → 成熟 → 废弃 → 归档** | `references/lifecycle.md` |
| **技能库运维与五维健康诊断** | **`skill-distribution` 的 `library-ops.md`** |
| ⭐ **审计清单（逐项打分）** | `references/audit.md` |

## Critical Rules

- ⭐ **扫描器的 SAFE 不等于安全**——先确认实际启用了几个引擎
- ❌ 只因"官方来源"就不审计——供应链攻击专挑热门包
- ❌ 跳过"小技能"——10 行脚本里一个 `eval()` 就够
- ❌ 只审代码不审 Markdown——SKILL.md 里的注入是真实向量
- ⭐ **每个版本都要独立重新审计**
- ⭐ **安全扫描只警告不阻断**——误报率高时自动阻断会侵蚀信任
- ⭐ **日志管道本身就会成为泄露源**——目标是"让 prompt 可 diff，但不可读"
- 一定要记 `top_k`——RAG 回归常常是它从 5 悄悄变成 20
- ⭐ 合规核心：**你必须能在事后证明"哪个 agent 做了什么"**
- 部署者日志**留存 ≥6 个月**
- ⭐ 网络白名单靠注入 `HTTP_PROXY`；**`/tmp` 永远不挂宿主机路径**

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "扫描器显示 SAFE" | SAFE ≠ 安全。先确认启用了几个引擎。 |
| "这是官方仓库的技能" | 供应链攻击专挑热门包。官方也要审。 |
| "就 10 行脚本，不用审" | 10 行里一个 eval() 就够。 |
| "上个版本审过了" | 每个版本都要独立验证。 |
| "多记点日志方便排查" | 日志管道本身是泄露源。让 prompt 可 diff 但不可读。 |
| "安全扫描要阻断合并" | 误报率高时自动阻断会侵蚀信任。只警告。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 含硬编码凭据/绝对路径检测
python scripts/estimate_tokens.py ./my-skill     # 量化上下文占用
```
