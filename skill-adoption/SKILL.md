---
name: skill-adoption
description: 让团队真正用起技能库——冷启动首个用例的选择、组织推广为什么推不动、团队约定与 PR 评审清单、仓库结构与共享流程、命名防冲突、采用度量（先行 vs 滞后指标）、准入标准与安全说明落地。用于推动同事用起来、建立共享库、度量采用情况，或处理"装了但没人用"。
  Do NOT use for 打包发布与版本回滚（用 skill-distribution）、企业注册中心与权限边界（用 skill-governance）、技能内容质量打分（用 skill-evaluating），也不用于个人自用技能。
---

# 团队采用与推广

## 边界

- 用于：**冷启动** · **组织推广** · **团队约定与 PR 流程** · **仓库结构** · **命名防冲突** · **采用度量** · **准入标准**
- 不用于：打包与版本 · 企业注册中心 · 质量打分 · 个人自用

## 核心原则

> ⭐ **多数技能计划不是死在代码里，是死在组织里。**

```
□ 一次微妙的错误，会让人退回手工⭐ 并告诉两个同事
□ ⭐ 如果"技能输出不对"的唯一回应是放弃它、退回临时提示词
   → 你的库会腐烂
□ ⭐ 如果有一条快速、无责怪的提交修复路径
   → 每次失灵都变成小改进，信任复利式增长
```

> ⭐⭐⭐ **推广卡在第一次体验。** 入门任务必须专门挑 agent 擅长的——
> **范围明确、机械化、高上下文**，且 ⭐ **错了只是烦人，不是灾难**。

## 何时不用本技能

- 打包、版本、tag 回滚 → `skill-distribution`
- 企业注册中心、RBAC、权限边界 → `skill-governance` 的 `skill-distribution/references/enterprise-registry.md`
- 技能本身质量打分 → `skill-evaluating`

## 路由表（按需深读）
| `skill-adoption/references/adoption-playbook-six-steps.md` | ⭐⭐⭐⭐ 六步采用；⭐⭐⭐ 首个用例四条件（含"错了只烦人"）；阻力最小路径 |
| `skill-adoption/references/cold-start.md` | ⭐⭐⭐ 冷启动：⭐⭐⭐ 别从最棘手的任务开始 |
| `skill-adoption/references/team-admission-criteria.md` | ⭐⭐⭐ 14 步流程 + 准入标准；⭐⭐⭐ 安全说明只写给人看 = 不存在 |
| `skill-adoption/references/team-conventions-pr.md` | ⭐⭐⭐ 团队约定四原则 + PR 评审清单 + 等级分层 |
| `skill-adoption/references/team-landing-seven.md` | ⭐⭐⭐ 七原则 + 三层分发 + ⭐ stable/dev 标签回滚 |
| `skill-adoption/references/team-naming-collisions.md` | ⭐⭐⭐ 防冲突命名 + 按环境拆分 + 四步上手 |
| `skill-adoption/references/adoption-metrics.md` | ⭐⭐⭐ 推广度量：先行/滞后指标 + 毕业信号四条 |
| `skill-adoption/references/team-repo-structure.md` | ⭐⭐⭐ 团队仓库结构 / profiles / CI 验证 |
| `skill-adoption/references/team-sharing.md` | ⭐⭐⭐ PR 四项评审 + 三作用域 |
| `skill-adoption/references/team-workflow.md` | ⭐⭐ 团队协作：指令与数据分离 |
| `skill-adoption/references/team-adoption.md` | ⭐⭐ 组织推广：为什么推不动 |
| `skill-adoption/references/adoption-playbook.md` | ⭐⭐ 前 30 天手册 / 冠军 / 规范 |

**冷启动**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 第一个用例选什么 | `skill-adoption/references/cold-start.md` · `skill-adoption/references/adoption-playbook-six-steps.md` |
| ⭐ 为什么推不动 | `skill-adoption/references/team-adoption.md` |
| 前 30 天怎么安排 | `skill-adoption/references/adoption-playbook.md` |

**建制度**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 团队约定与 PR 清单 | `skill-adoption/references/team-conventions-pr.md` |
| ⭐ 准入标准（安全说明落地） | `skill-adoption/references/team-admission-criteria.md` |
| 仓库结构与共享 | `skill-adoption/references/team-repo-structure.md` · `skill-adoption/references/team-sharing.md` |
| 命名防冲突 | `skill-adoption/references/team-naming-collisions.md` |
| 三层分发与回滚标签 | `skill-adoption/references/team-landing-seven.md` |

**看效果**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 采用度量（别测错东西） | `skill-adoption/references/adoption-metrics.md` |

## Critical Rules

- ⭐ 入门任务要专门挑 **agent 擅长**的（范围明确、机械化、高上下文）
- ⭐⭐ **首个用例必须"错了只是烦人"**——不是灾难（两条独立来源同证）
- 提供**开箱即用的团队配置**（MCP + 技能 + hooks），而不是让新人从空白开始
- ⭐ **评审严格度不下降**——明确说在前面，防止"AI 做的就橡皮图章"
- ❌ **不要按指标强制使用**——产出的是刷数据，不是推广
- ⭐⭐⭐ **安全说明写在 README = 不存在**（agent 读不到）——必须写进正文流程
- ⭐ stable/dev 标签让回滚变成"移动指针"，成本几乎为零

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "大家装上自然会用" | ⭐ 推广卡在第一次体验。入门任务必须精选。 |
| "先从最难的问题开始，证明它的价值" | ⭐⭐ 工程师把 agent 用在最棘手的任务上，于是断定这工具还不行。 |
| "团队里发个链接就行" | 没有 PR 评审和修复路径的技能库会腐烂。 |
| "安全说明写在 README 里了" | ⭐⭐⭐ README 不在加载链里，agent 根本读不到。 |
| "按使用次数考核" | 产出的是刷数据。看滞后指标（返工率、自建数）。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 准入校验（结构、路由、行数） |
| `scripts/estimate_tokens.py <dir>` | 记录成本基线 |

## 参考

- 相关技能：《skill-distribution》（打包与版本）·《skill-governance》（注册中心与权限）·
  《skill-evaluating》（质量打分）
