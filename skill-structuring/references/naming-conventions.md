# 命名约定：name 同时是标识符、搜索关键词、认知锚点

> 相关：《skill-structuring》的 `frontmatter-fields.md` ·
> `cross-agent-portability.md` · 《skill-authoring》的 `description-writing.md`

---

## 目录

- [1. ⭐ 三重角色](#1--三重角色)
- [2. 硬规则](#2-硬规则)
- [3. ⭐ 推荐形态：动名词](#3--推荐形态动名词)
- [4. ⭐ 一致性比形态更重要](#4--一致性比形态更重要)
- [5. 正反例](#5-正反例)

---

## 1. ⭐ 三重角色

> ⭐ **技能名称同时承担：标识符 · 搜索目标 · 认知锚点。**

```
标识符    机器解析用
⭐ 搜索关键词  ⭐ agent 检索技能时，name 本身参与相似度与关键词匹配
认知锚点  人和 agent 看到名字就能大致理解核心意图与适用场景
```

> ⭐ 第三条最容易被忽略，也最实用：
> **如果你用的是人类和 agent 都自然会搜索的词汇，被找到的机会就显著提高。**

---

## 2. 硬规则

```
① 小写 kebab-case
② ⭐ 只允许字母、数字、连字符（不允许括号与特殊字符）
③ ⭐ ≤64 字符
④ ⭐ ⭐ 不得含保留词 "anthropic" / "claude"
⑤ ⭐ 不得用会自动添加的前缀（如 posthog-*，由消费方 agent 添加）
```

> ⭐ 第 ④ 条的后果最隐蔽：
> **其他客户端都能正常加载，只有 Claude 静默拒收。**

**为什么 kebab-case 不是风格偏好而是协议**：

```
⭐ 它为解析器提供无歧义的 token 分隔
```

一个真实教训：**接入某 registry 时，所有 camelCase 命名的技能注册后全部失效——
不是报错，而是根本无法被 Planner 发现。**

---

## 3. ⭐ 推荐形态：动名词

| 形态 | 例子 | 评价 |
|---|---|---|
| ⭐ **动名词（首选）** | `querying-posthog-data` · `exploring-llm-traces` · `managing-feature-flags` | ⭐ 首选 |
| 名词短语（可接受） | `error-tracking-guide` | 可接受 |
| 动作导向（可接受） | `process-pdfs` · `analyze-spreadsheets` | 可接受 |

**用动作或核心洞察命名，不用模糊类别**：

```
✅ flatten-with-flags
❌ data-structure-refactoring
```

**语义匹配要求名称携带"领域动词 + 宾语 + 限定词"**：

```
✅ calculate-tax-rate-for-ecommerce-order
❌ process-order
```

---

## 4. ⭐ 一致性比形态更重要

> ⭐ **命名集合内的一致性，比具体选哪种形态更关键。**

```
❌ 一个叫 writing-workflow-sops，下一个叫 sop-writer，第三个叫 create-sops
✅ 选定一个模式，整套库都用它
```

一致的命名让技能**更易在文档中引用、一眼能懂、可搜索、可维护**。

**避免的模式**：

| 模式 | 例子 | 原因 |
|---|---|---|
| 含糊 | `helper` · `utils` · `tools` | 完全看不出做什么 |
| ⭐ 过于泛化 | `documents` · `data` · `files` | 太宽，没用 |
| 保留词 | `anthropic-helper` · `claude-tools` | ⭐ 平台阻止 |
| 混用模式 | `writing-docs` 与 `pdf-processor` 并存 | 制造混淆 |

**一个真实的功能重叠事故**：

```
risk-assessment 与 credit-score-calculation 功能重叠率 80%
⭐ 只因命名未体现输入约束——
   前者接受企业财报，后者只处理个人征信
⭐ 导致 Planner 随机调用，引发合规风险
```

> ⭐ **命名不是开发完成后的补丁，而是设计阶段就必须锁定的契约。**

---

## 5. 正反例

```
❌ name: helper          description: 'Helps with stuff'
❌ name: llm-analytics   —— 一把伞，覆盖 traces/experiments/evals/cost/prompt
✅ name: exploring-llm-traces   —— 聚焦一个工作流

✅ querying-posthog-data：
   · 声明它依赖的精确 MCP 工具
   · 解释事件层级与如何通过 $ai_parent_id 链接
   · 走具体工作流（从 URL 调试、成本分析、工具使用验证）
   · 渐进式披露——完整 schema 放 references/
   · ⭐ 带预写好的 Python helper 脚本
     ⭐ agent 直接跑，不用重新推导 JSON 形状、手工切嵌套载荷
     ⭐ ——这既简化了轨迹，又让上下文窗口保持干净
```

> ⭐ 最后那条值得单独记：**"预写好脚本"的价值不只是省 token，
> 更是让 agent 不必"探索式解析"——那正是轨迹变脏的来源。**

---

## 速查

```
□ 小写 kebab-case
□ ⭐ 只含字母数字连字符
□ ≤64 字符
□ ⭐ 不含 anthropic / claude
□ ⭐ 不用会被自动添加的前缀

□ ⭐ 首选动名词（verb + -ing）
□ 用动作/核心洞察命名，不用模糊类别
□ ⭐ 名称携带"领域动词 + 宾语 + 限定词"
□ ⭐ 集合内一致 > 具体形态
□ ❌ helper / utils / documents 这类含糊名
□ ⭐ 命名是设计阶段锁定的契约，不是事后补丁

□ ⭐ 好技能：聚焦一个工作流 + 声明精确依赖 + 预写脚本
□ ❌ 坏技能：一把伞覆盖所有相关主题
```

**一句话**：

> ⭐ **如果你用的是人类和 agent 都自然会搜索的词汇，
> 技能被找到的机会就会显著提高——可以把命名视为 CSO 的一部分。**
