---
name: skill-domain-infra
description: 基础设施与数据领域 Agent Skills 的实例库——DevOps/SRE、可观测运维、事故分诊、日志分析、数据分析、数据工程、数据管道、数据库/SQL、数据可视化、ML/MLOps、性能优化、事件驱动架构、C4 架构图、无障碍、设计系统、语言审阅、研究方法、安全测试与安全域。用于按领域参考现成写法，或把本领域的工程规范沉淀成技能。
  Do NOT use for 软件开发与代码类领域（用 skill-domain-eng）、业务运营类领域（用 skill-domain-biz）、技能本身的写法与流程（用 skill-authoring）、评估打分（用 skill-evaluating），也不用于直接产出工程交付物。
---

# 基础设施与数据领域实例库

> 姊妹技能：**`skill-domain-eng`**（软件开发与代码类）

## 边界

- 用于：**按基础设施/数据领域参考现成写法** · **把本领域规范沉淀成技能**
- 不用于：软件开发与代码领域 · 业务运营领域 · 技能写法本身 · 评估打分 · 直接产出交付物

## 核心原则

> ⭐ **这些实例共同的价值**：
> **基础设施类任务错了代价极高——把安全阀写进技能，而不是留在每个人脑子里。**

```
□ 运维类技能：先只读，确认稳定后再开放写操作
□ 数据分析类：确定性计算交给脚本，语义判断交给模型
□ 安全类：给出可自动检查的谓词，不给形容词
```

## 路由表（按需深读，不要一次全读）
| `game-perf-mobile.md` | ⭐ 手游性能：量化目标线、静态合批教训、GC 尖峰 |
| `gamedev-asset-pipeline.md` | ⭐ 游戏资产流水线：模型+脚本分工的极端样本 |
| `monorepo-skills.md` | monorepo 结构与技能发现 |

### 运维与可靠性
| `devops-skills.md` | 渐进式放权先只读、Error Budget 冻结规则 |
| `observability-ops-skills.md` | 可观测运维 |
| `incident-triage.md` | 事故分诊 |
| `log-analysis.md` | 日志分析 |
| `performance-optimization.md` | 先测量再优化、低于 5% 就回滚 |
| `soc-soar-skills.md` | 安全运营 |

### 数据
| `data-analytics.md` | 数据分析类：七步构建法、模型 vs 脚本分工 |
| `data-engineering-skills.md` | 先写数据契约、七条假设反驳 |
| `data-pipeline-skills.md` | 数据管道 |
| `database-sql-skills.md` | 数据库 / SQL |
| `schema-migration-skills.md` | schema 迁移 |
| `data-viz-skills.md` · `data-viz-selection.md` | ⭐ 图表选择表与四个 gotcha |

### ML
| `ml-mlops-skills.md` | ML/MLOps |
| `ml-feature-engineering.md` | 特征工程 |

### 架构
| `event-driven-architecture.md` | 事件驱动选型表 |
| `c4-architecture-diagram.md` | C4 架构图 |

### 质量与研究方法
| `a11y-skills.md` | ⭐ 无障碍：自动化只抓 30–57% |
| `design-system-skills.md` | Token 三层、可自动检查的验收清单 |
| `language-reviewer-skills.md` | 语言审阅 |
| `research-skills.md` | ⭐ 五条硬护栏、禁止编造引用 |
| `security-domains.md` · `security-review-checklist.md` · `security-testing-skills.md` | 安全测试与风险排序 |

## 使用方式

1. **确认领域**：你要做的是基础设施/数据类，还是软件开发类（→ `skill-domain-eng`）。
2. **读对应实例**：路由表按需深读，一次只读一份。
3. **提炼成自己的技能**：参考实例的章节结构与判据写法。
4. **补 Gotchas**：⭐ 把你们真实踩过的坑写进去——这是最难被替代的部分。

## 常见借口

| 借口 | 反驳 |
|---|---|
| "运维流程太特殊，没法写成技能" | 正因特殊才要写——否则全靠记性 |
| "照着实例抄一份就行" | ⭐ 实例给的是结构与判据，你们的 Gotchas 才是价值 |
| "数据分析直接让模型算就行" | ⭐ 计算进脚本，语义判断才交给模型 |

其余见 `skill-authoring` 的 `references/anti-rationalizations.md`。
