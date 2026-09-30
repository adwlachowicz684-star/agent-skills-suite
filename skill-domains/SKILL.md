---
name: skill-domains
description: 按业务领域写 Agent Skills——代码评审、测试、文档、研究方法、Git/PR 工作流、日志与事故分诊、性能优化、重构、依赖升级、monorepo、Schema 迁移、CLI 设计、国际化、遗留现代化、客户支持、会议纪要、PM、采购 RFP、电商运营、ML/MLOps、SOC/SOAR、合规、品牌规范、组织上下文等 30 多个领域的技能设计要点。用于为某个具体职能或行业定制技能时查该领域的特有约束、输出契约与陷阱。
  Do NOT use for 通用的技能设计原则与反模式（用 skill-patterns）、完整可抄的技能源码（用 skill-gallery）、拆分与瘦身决策（用 skill-refining），也不用于领域本身的业务知识问答。
---

# 按领域写技能

## 边界

- 用于：**某个具体职能/行业**的技能该怎么写（特有约束、输出契约、领域陷阱）
- 不用于：通用设计原则与反模式 → 《skill-patterns》
- 不用于：完整源码样本 → 《skill-gallery》
- 不用于：拆分与瘦身决策 → 《skill-refining》

## 核心原则

> ⭐⭐⭐⭐ **领域技能的价值不在"覆盖了这个领域"，在"知道这个领域的坑"。**

```
□ ⭐⭐⭐⭐ 通用部分（流程骨架、输出格式）各领域差不多
   → ⭐⭐⭐⭐⭐ 差别全在领域特有的失败模式
□ ⭐⭐⭐⭐ 一个"代码评审技能"如果只是"读 diff 给建议"，
   那它和通用提示词没区别
□ ⭐⭐⭐⭐⭐ 判据：去掉领域名，这份技能还剩什么？
```

> ⭐⭐⭐⭐ **领域技能最容易犯的错是把领域知识写进去。**
> 技能该写的是⭐⭐⭐⭐⭐ **"这个领域里，模型默认会做错的那几件事"**——
> 而不是这个领域是什么。

## 路由表（按需深读）

**工程**：

| `skill-domains/references/code-review-automation.md` | ⭐⭐⭐⭐ 评审技能的结构与输出分级 |
| `skill-domains/references/code-review-trust.md` | ⭐⭐⭐⭐⭐ 评审可信度：假阳性比漏报更伤信任 |
| `skill-domains/references/testing-skills.md` | ⭐⭐⭐ 测试类技能 |
| `skill-domains/references/code-quality-skills.md` | ⭐⭐⭐ 代码质量类 |
| `skill-domains/references/refactoring-skills.md` | ⭐⭐⭐ 重构类：⭐ 必须先有测试基线 |
| `skill-domains/references/legacy-modernization.md` | ⭐⭐⭐ 遗留现代化 |
| `skill-domains/references/dependency-upgrade.md` | ⭐⭐⭐⭐ 依赖升级：⭐⭐⭐⭐ 破坏性变更要按 changelog 逐条核对 |
| `skill-domains/references/performance-optimization.md` | ⭐⭐⭐⭐ 性能优化：⭐⭐⭐⭐ 必须先测量，禁止凭直觉改 |
| `skill-domains/references/build-error-resolution.md` | ⭐⭐⭐ 构建错误排查 |
| `skill-domains/references/debugging-recovery.md` | ⭐⭐⭐ 调试与恢复 |
| `skill-domains/references/monorepo-skills.md` | ⭐⭐⭐⭐ monorepo：⭐⭐⭐⭐⭐ 作用域限定（paths）是这类技能的关键 |
| `skill-domains/references/schema-migration-skills.md` | ⭐⭐⭐⭐ Schema 迁移：⭐⭐⭐⭐⭐ 不可逆，必须 dry-run |
| `skill-domains/references/cli-design-skills.md` | ⭐⭐⭐ CLI 设计 |
| `skill-domains/references/i18n-implementation.md` | ⭐⭐⭐ 国际化实现 |
| `skill-domains/references/security-review-checklist.md` | ⭐⭐⭐ 安全评审清单 |

**协作与流程**：

| `skill-domains/references/git-pr-workflow.md` | ⭐⭐⭐⭐ Git/PR 工作流 |
| `skill-domains/references/changelog-release-notes.md` | ⭐⭐⭐ CHANGELOG 与发布说明 |
| `skill-domains/references/incident-triage.md` | ⭐⭐⭐⭐⭐ 事故分诊：⭐⭐⭐⭐⭐ 时效优先于完整，先止血后归因 |
| `skill-domains/references/log-analysis.md` | ⭐⭐⭐ 日志分析 |
| `skill-domains/references/meeting-notes-action.md` | ⭐⭐⭐⭐ 会议纪要与行动项：⭐⭐⭐⭐ 缺责任人和时间就是不合格 |
| `skill-domains/references/stakeholder-comms.md` | ⭐⭐⭐ 干系人沟通 |
| `skill-domains/references/documentation-skills.md` | ⭐⭐⭐ 文档类 |
| `skill-domains/references/api-doc-generation.md` | ⭐⭐⭐ API 文档生成 |
| `skill-domains/references/research-skills.md` | ⭐⭐⭐⭐ 研究类：⭐⭐⭐⭐⭐ 引用必须可追溯，禁止编造来源 |
| `skill-domains/references/methodology-skills.md` | ⭐⭐⭐⭐ 方法论类：⭐⭐⭐⭐ 流程顺序不可打乱 |
| `skill-patterns/references/feedback-loop-design.md` | ⭐⭐⭐ 反馈回路设计 |

**业务职能**：

| `skill-domains/references/customer-support-skills.md` | ⭐⭐⭐⭐ 客户支持：⭐⭐⭐⭐⭐ 不可承诺未授权事项 |
| `skill-domains/references/pm-skills.md` | ⭐⭐⭐⭐ PM 类 |
| `skill-domains/references/ecommerce-ops-skills.md` | ⭐⭐⭐ 电商运营 |
| `skill-domains/references/procurement-rfp.md` | ⭐⭐⭐ 采购与 RFP |
| `skill-domains/references/ml-mlops-skills.md` | ⭐⭐⭐⭐ ML/MLOps：⭐⭐⭐⭐ 数据漂移与可复现性 |
| `skill-domains/references/soc-soar-skills.md` | ⭐⭐⭐⭐ SOC/SOAR 安全运营 |
| `skill-domains/references/vertical-compliance.md` | ⭐⭐⭐⭐⭐ 垂直行业合规：⭐⭐⭐⭐⭐ 保守输出优于自信输出 |
| `skill-domains/references/brand-guidelines.md` | ⭐⭐⭐ 品牌规范 |
| `skill-domains/references/writing-org-context.md` | ⭐⭐⭐⭐ 组织上下文：⭐⭐⭐⭐ 缩写与内部术语是最大价值点 |

## Critical Rules

- ⭐⭐⭐⭐⭐ **不可逆动作必须 dry-run + 显式确认**（Schema 迁移、删除、发外部通知）
- ⭐⭐⭐⭐ **先测量后优化**——性能优化类技能里"凭直觉改"是最常见的领域错误
- ⭐⭐⭐⭐⭐ **研究/引用类技能必须有可追溯来源**，找不到就写"无"，不得编造
- ⭐⭐⭐⭐ **合规与法律相关领域默认保守**：说"不确定"优于给一个自信的答案
- ⭐⭐⭐⭐ monorepo 类技能用 `paths:` 限定作用域（见《skill-loading》）
- ⭐⭐⭐⭐ 会议纪要/行动项类：缺责任人或截止时间即为不合格输出
- ⭐⭐⭐⭐ 事故分诊类：时效优先于完整，**先止血后归因**
- ⭐⭐⭐ 不要把领域百科写进技能——会腐烂（见《skill-refining》的 `skill-refining/references/memory-layering-and-skills.md`）

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "我把这个领域的最佳实践都写进去了" | ⭐⭐⭐⭐ 那是百科。技能要写的是"模型会做错的几件事"。 |
| "这个领域没有特殊之处" | ⭐⭐⭐⭐ 去掉领域名还剩什么？如果没剩，它不该是一个独立技能。 |
| "事故分诊要全面分析" | ⭐⭐⭐⭐⭐ 时效优先。先止血后归因，完整分析是事后复盘的事。 |
| "找不到来源就先给个类似的" | ⭐⭐⭐⭐⭐ 编造来源在研究类技能里是最严重的失败。 |
| "迁移有回滚所以不用 dry-run" | ⭐⭐⭐⭐ 数据类迁移往往没有真正可用的回滚。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验 |
| `scripts/estimate_tokens.py <dir>` | 成本基线 |

## 参考

- 相关技能：《skill-patterns》（通用设计原则与反模式）·《skill-gallery》（完整源码样本）·
  《skill-crafting》（措辞与示例写法）·《skill-refining》（拆分与瘦身）
