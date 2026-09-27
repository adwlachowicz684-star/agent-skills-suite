---
name: skill-domain-biz
description: 业务运营领域 Agent Skills 的实例库——产品管理、合同审查、客服知识库、营销/SEO/文案、财务会计、招聘/HR、电商供应链、游戏开发、方法论编码、个人知识管理、组织语境写作。用于按业务领域参考现成写法，或把本部门的业务规则与隐性经验沉淀成技能。
  Do NOT use for 工程技术领域（用 skill-domain-eng）、技能本身的写法（用 skill-authoring）、评估打分（用 skill-evaluating），也不用于直接产出业务交付物。
---

# 业务运营领域实例库

## 边界

- 用于：**按业务领域参考现成写法** · **把业务规则与隐性经验沉淀成技能**
- 不用于：工程技术领域 · 技能写法本身 · 评估打分 · 直接产出交付物

## 核心原则

> ⭐ **这类技能的目标不是"更聪明"，而是"不出错"。**

```
□ ⭐ 判断标准：一致性是否比创造性重要？
   是 → 做成技能；要的是创意 → 别做，会束缚它
□ ⭐ 强依赖组织内部语境的（脱离就失真）→ 尤其适合
□ ⭐ 把个人经验转化为组织可复用的生产力资产
```

> ⭐ **通用判据：四步结构**
> **收集信息 → 判断条件 → 执行操作 → 生成结果**
> 只要流程符合这四步且有明确业务规则，就能实现自动化。
> ⭐ 尤其是**依赖资深员工经验、难以标准化交接**的任务。

## 路由表（按需深读，一次只读一份）
| `okr-metrics.md` | ⭐ 业务指标：挂业务 KPI，场景→权重→避坑重点 |

| 领域 | 读 |
|---|---|
| 产品管理（PRD 九要素、模式路由） | `references/pm-skills.md` |
| ⭐ 合同审查（五 Agent 流水线、克制原则） | `references/legal-contract-skills.md` |
| ⭐ 客服 / 知识库问答（四块输出、升级规则） | `references/customer-support-skills.md` |
| 营销 / SEO / 文案（安装量最大的一批） | `references/marketing-seo-skills.md` |
| 财务 / 会计 / 结账报告 | `references/finance-accounting-skills.md` |
| ⭐ 招聘 / HR（含四条合规边界） | `references/hr-recruiting-skills.md` |
| 电商 / 供应链 / 企业流程 | `references/ecommerce-ops-skills.md` |
| 游戏开发（引擎规范 / 工作室编排） | `references/game-dev-skills.md` |
| 成熟方法论编码（文案公式选择表） | `references/methodology-skills.md` |
| 个人知识管理 / 第二大脑 | `references/pkm-skills.md` |
| ⭐ **CRM / 销售：十类工作流与人工把关** | `references/crm-sales-skills.md` |
| ⭐ **A/B 测试与增长实验（ICE、实验手册、节奏）** | `references/ab-testing-growth.md` |
| ⭐ **供应商评估：0/3/5 打分与红旗清单** | `references/procurement-rfp.md` |
| ⭐ **市场调研与竞品分析：证据分级** | `references/market-research-skills.md` |
| ⭐ **客户成功：健康分、生命周期、分级告警** | `references/customer-success-playbook.md` |
| ⭐ **会议纪要转行动项（置信度标记）** | `references/meeting-notes-action.md` |
| **UX 文案与微文案（错误/空状态/禁词）** | `references/ux-writing-microcopy.md` |
| **资助申请书：十段结构与评审对齐** | `references/grant-proposal.md` |
| ⭐ **品牌规范：常量该写进正文，验证交给脚本** | `references/brand-guidelines.md` |
| ⭐ **OKR 与目标：KR 可判定性检查、哪些必须留人** | `references/okr-planning.md` |
| ⭐ **培训与入职：练习与检验，不是讲义** | `references/training-onboarding.md` |
| ⭐ **干系人沟通：按受众重组、必须有未确认清单** | `references/stakeholder-comms.md` |
| **问卷设计与调研分析** | `references/survey-research.md` |
| ⭐ **定价与包装：价值指标优先** | `references/pricing-packaging.md` |
| **内容运营：选题、一稿多用、编辑检查单** | `references/content-operations.md` |
| ⭐ **垂直合规：金融 / 医疗 / 法务** | `references/vertical-compliance.md` |
| 文档写作与组织语境（六类高价值场景） | `references/writing-org-context.md` |

## Critical Rules

**业务技能的红线**：

- ⭐ **不得承诺退款、赔偿、折扣**——这些必须进入人工复核
- ⭐ **匹配评分必须可解释**——给出"匹配度 + 缺口项"；只给一个黑箱分数无法申诉
- ⭐ **不得使用受保护特征**（性别、年龄、民族、婚育状况）
- ⭐ **模型可以组织数字，不能生成数字**（财务类）
- ⭐ 知识库字段至少含：**问题类型 · 适用产品 · 规则原文 · 生效时间**
- ⭐ 不要把过期价格表混进知识库——会生成"看似专业但实际错误"的回复
- 复杂投诉：先整理事实，再交负责人；不自动回复

**结构要点**：

- ⭐ 输出要**拆成多块**（客户回复 / 内部动作 / 风险提示 / 复盘字段），不要写成一整段
- ⭐ 升级规则必须是**可判定条件**（三次远程排查失败 / 出现硬件异常码）
- ⭐ 指标定义必须含**计算逻辑 + 边界条件 + 常见误读**
- 品牌规范要含四件事：**语气基准 · 术语表 · 禁用词 · 示例库**
- 权重、阈值等组织口径**放在数据文件里**，不写死在技能里
- ⭐ 用齐 `SKILL.md`（流程）+ `scripts/`（确定性）+ `templates/`（模板）+ `references/`（规则）

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "直接给出匹配分数就行" | ⭐ 黑箱评分无法申诉。必须带缺口项。 |
| "让 agent 直接承诺折扣能更快成交" | ❌ 退款/赔偿/折扣必须人工复核。 |
| "客服回复写一段就好" | 要拆成四块——内部动作与风险提示不能省。 |
| "业务规则写死在技能里更省事" | 权重与阈值会变。放数据文件里独立更新。 |
| "这个任务很有创造性，也做成技能" | ⭐ 一致性 > 创造性才适合。否则会束缚它。 |
| "命中率高说明技能好" | 业务技能看的是"不出错"，不是"能触发"。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验
python scripts/estimate_tokens.py ./my-skill     # 估算成本
```
