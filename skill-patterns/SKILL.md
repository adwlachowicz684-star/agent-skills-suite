---
name: skill-patterns
description: >
  按任务类型归纳的技能设计范式库。当你要做的技能属于某一类常见任务
  （测试、文档、评审、重构、调试、迁移、研究、安全清单、运维分诊、内容、
  客服、PM、合规、采购打分、会议记录、指标…），或你想知道「这类技能
  该装什么、骨架长什么样、哪些规则值得编码」时使用。
  提供每类技能的骨架、必编码项、判定表与反模式，可直接照着改。
  不用于：从零写第一个技能（用 `skill-authoring`）、正文构件写法
  （用 `skill-crafting`）、评估与治理（用 `skill-evaluating` /
  `skill-governance`）、也不提供各领域的技术知识本身（如 SQL 索引、
  图表选型、引擎 API）。
---

# 技能设计范式库

> 定位：**按任务类型归纳「这类技能该怎么设计」**。
> 每份讲骨架、必编码项、判定表、反模式——**领域只是载体，方法通用**。
> 若要找「怎么从零写一个技能」，去 `skill-authoring`。

## 强制工作流

1. **确认任务类型**——用户要做的技能属于哪一类？
2. **读对应范式**（下面路由表；不确定就读 `methodology-skills`）
3. ⭐ **重点看三个部分**：骨架 · 必编码项 · 反模式
4. **套用判定表**——把「模型自己猜」变成「查表」
5. **补 Gotchas**——你团队踩过的坑，这是技能最有价值的部分
6. **跑 `validate_skill.py`**，然后跑 5+5 触发测试

## 路由表
| `four-design-principles-io-contract.md` | ⭐⭐⭐⭐ 四项原则；★★无状态此前未列为原则 + schema.yaml 数据契约 |
| `conflict-precedence-four-types.md` | ⭐⭐⭐ 四层优先级(事实是约束/技能是指导)+四种冲突类型 |
| `shared-service-skill.md` | ⭐⭐⭐ 共享服务技能：总是返回有效输出或明确错误 |
| `seven-anti-patterns-scale.md` | ⭐⭐ 规模化七反模式；⭐⭐⭐ Markdown 指令不是访问控制 |
| `skill-families-nine.md` | ⭐⭐ 九类技能；跨类最难用好，一类做到底 |
| `solid-for-skills.md` | ⭐ 软件设计原则迁移：SOLID 映射、两张图、组合代价 |
| `why-six-layers.md` | ⭐ 六层结构：目标/输入/流程/格式/自检/FAQ |
| `skill-overrides-audit.md` | ⭐ 同名覆盖与冲突：三级命名空间、审计、my- 前缀 |
| `skeleton-template.md` | ⭐ 可直接抄的骨架（六必含小节 + 触发调优） |
| `instruction-craft.md` | ⭐ 正文写作：祈使句、钉死格式、讲为什么 |
| `context-budget-math.md` | ⭐ 预算算术：96% 从哪来、压缩会驱逐技能 |
| `team-registry-governance.md` | ⭐ 团队分发：manifest、pin、owner、hub-and-spoke |
| `structure-modes-abcde.md` | ⭐ 五种结构模式 A–E（含各自行数目标） |
| `six-step-creation.md` | ⭐ 六步创建法 + 五阶段学习路径 |
| `publish-checklist-20.md` | ⭐ 发布前 20 项（0–2 分制，28 分才发） |
| `golden-rules-failure-modes.md` | ⭐ 黄金规则：每条失败模式配一条机械规则 |
| `feedback-loop-design.md` | ⭐ 反馈环：做→检查→修，规则升级为代码 |
| `ten-common-mistakes.md` | ⭐ 十条常见错误与四条最该记住的 |
| `skill-type-testing.md` | ⭐ 按类型选测法（Pattern 测 near-miss、Discipline 加压力） |
| `review-checklist.md` | ⭐ 十项自检 + 反转测试 + 只记三条 |
| `nine-anti-patterns.md` | ⭐ 九个反模式：症状 / 根因 / 修法 |
| `meta-skill-factory.md` | ⭐ 元技能：让 agent 自己写技能（含人在环路） |
| `knowledge-delta-checklist.md` | ⭐ 知识增量清单：该有的是模型不知道的 |
| `five-design-patterns.md` | ⭐⭐ 五种设计模式 + 选型决策树（Tool Wrapper 起步） |

| 文档 | 内容 |
|---|---|
| `methodology-skills.md` | ⭐⭐ 成熟人类方法论如何变成技能（公式选择表 = 决策树） |
| `testing-skills.md` | ⭐ 测试类 ROI 最高：必须编码的三件事 |
| `code-quality-skills.md` | ⭐ 骨架：核心规则 + 语言差异表 + 严重度分级 |
| `documentation-skills.md` | ⭐ 核心是更易审计，不是写得更长 |
| `refactoring-skills.md` | ⭐ 代码味道 → 重构手法对照表 |
| `code-review-automation.md` | ⭐ 评审自动化的分层信任工作流 |
| `code-review-trust.md` | ⭐ 评审价值 = 发现能力 × 信任程度 |
| `git-pr-workflow.md` | ⭐ 三个小技能组成循环：小而尖靠组合 |
| `debugging-recovery.md` | ⭐ 五步分诊 + 两条护栏 |
| `build-error-resolution.md` | 禁止猜测式修改 |
| `dependency-upgrade.md` | ⭐ 关键是证明没弄坏东西 |
| `changelog-release-notes.md` | ⭐ 确定性生成：不该交给模型自由发挥 |
| `cli-design-skills.md` | ⭐ 让你的 CLI 变得 agent 好用 |
| `i18n-implementation.md` | ⭐ 唯一可判定的完成标准 |
| `api-doc-generation.md` | ⭐ 输出模板定义一次，全队一致 |
| `legacy-modernization.md` | ⭐ 五阶段 + 绞杀者模式 |
| `monorepo-skills.md` | ⭐ 多语言仓库里技能放哪、避免互相干扰 |
| `research-skills.md` | ⭐ 研究类需要更强护栏 |
| `performance-optimization.md` | ⭐ 先测量再优化、改进 <5% 就回滚 |
| `incident-triage.md` | ⭐ 值得逐句读的真实技能样本 |
| `log-analysis.md` | ⭐ 强制证据链 |
| `security-review-checklist.md` | ⭐ 清单怎么组织才真的会被执行 |
| `soc-soar-skills.md` | ⭐ 把能自动和该自动分开 |
| `ml-mlops-skills.md` | ⭐ 反复犯同样错误 → 编码成铁律 |
| `schema-migration-skills.md` | ⭐ 自由度校准里该给精确脚本的那一档 |
| `brand-guidelines.md` | ⭐ 数据放正文 vs 放脚本的分界 |
| `ecommerce-ops-skills.md` | ⭐ 判断流程值不值得做成技能的判据 |
| `procurement-rfp.md` | ⭐ 0/3/5 打分制：把主观变可判定 |
| `customer-support-skills.md` | ⭐ 为什么不能只靠提示词 |
| `pm-skills.md` | ⭐ 模式路由：先选对分支 |
| `writing-org-context.md` | ⭐ 目标是不出错而不是更聪明 |
| `stakeholder-comms.md` | ⭐ 最大风险是看起来专业但内容不对 |
| `meeting-notes-action.md` | ⭐ 确定性抽取 + 模型润色、置信度标记 |
| `vertical-compliance.md` | ⭐ 规则来自外部而非团队内部 |

## 通用规律（跨范式）

读任何一份前先看这四条，它们是所有范式的共性：

1. ⭐ **把「模型自己猜」变成「查表」**——判定表是最有效的编码形式
   （公式选择表、图表选择表、味道→手法表、框架选型表，都是这个）
2. ⭐ **确定性部分交给脚本**——能算的别让模型生成
   （Changelog、版本号、覆盖率、打分）
3. ⭐ **Gotchas 是最高信号**——来自真实踩坑，几乎不可能通过
   no-op 测试，修剪时永远别动它
4. ⭐ **写明「不做/不该用」**——没有边界的技能会被用错场景

## 何时不用（边界）

- ❌ **Do NOT** 用本技能查找领域技术知识本身——
  如「SQL 该不该建索引」「饼图最多几块」「Unity 的 Awake/Start 区别」。
  本技能讲的是**这类技能怎么设计**，不是领域答案。
- ❌ **Do NOT** 用本技能从零创建第一个技能——去 `skill-authoring`。
- ❌ **Do NOT** 用本技能查正文构件写法（形态、目录、脚本、验证）——
  去 `skill-crafting`。
- ❌ **Do NOT** 用本技能做评估、治理、安全合规——
  去 `skill-evaluating` / `skill-governance`。
- ❌ **Do NOT** 直接照抄范式而跳过第 5 步——
  **没有你团队 Gotchas 的技能是通用废话**。
