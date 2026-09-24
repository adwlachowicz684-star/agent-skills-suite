---
name: skill-crafting
description: 打磨 Agent Skill 的正文构件——指令形态、目录契约、脚本工程、输出契约、验证章节、错误处理、指令分层。用于禁令不管用、输出形状不稳、agent 跳步、脚本该不该抽、内容该放 SKILL.md 还是 AGENTS.md、怎么证明"完成了"。
  Do NOT use for 从零创建技能的整体流程（用 skill-authoring）、已有技能的瘦身拆分（用 skill-refining）、评估与打分（用 skill-evaluating），也不用于写一次性提示词。
---

# 技能正文的构件

## 边界

- 用于：**指令措辞与形态** · 目录与脚本组织 · 输出契约 · 验证章节 · 错误处理 · 指令分层
- 不用于：整体创建流程 · 瘦身拆分 · 评估打分 · 一次性提示词

## 核心原则

> ⭐ **同一个"要求"，写法错了就是废话；写法对了才是约束。**

| 失败形态 | ✅ 该用什么 | ❌ 常见错误（也是多数人的默认） |
|---|---|---|
| 明知故犯、赶工 | 禁令 + 借口反驳表 | 软指导 |
| **输出形状不对** | **正面配方**（模板 + 槽位） | **禁令清单** |
| 漏掉必需元素 | 模板里的 REQUIRED 槽位 | 散文提醒 |
| 依条件而定 | `if <可观察谓词> then` | 无条件规则 + 例外条款 |

> ⭐ **禁令可能比不写还糟**：禁令说"不能做什么"，但没说应该做什么。
> 实测中**禁令组比配方组产生了更多不想要的内容**，甚至比不写指导的对照组更差。
> → **默认不要伸手拿禁令**。

## 路由表（按需深读）
| `writing-style-rfc2119.md` | ⭐ RFC 2119 关键词 + 语义换行 + 20 词上限 |
| `skill-anatomy-antipatterns.md` | ⭐⭐ description 触发/正文教；绝不在 description 总结工作流 |
| `token-bloat-audit.md` | ⭐ 瘦六个动作：合并工具调用、/compact、抑制冗长输出 |
| `anti-patterns-catalog.md` | ⭐ 五类反模式总目（含模型已知信息、嵌套引用） |
| `script-cli-contract.md` | ⭐⭐ 脚本 CLI 契约：stdout/stderr、退出码分级、JSON 输出 |
| `write-reasons-not-rules.md` | ⭐ 写原因而非堆规则 + 三成原则 + 风险三档 |
| `content-layering-four.md` | ⭐ 四层沉淀：原则/知识/模板/动作各归其位 |
| `imperative-style.md` | ⭐ 祈使句 vs 第二人称 + 尺寸分级 + 评分权重 |
| `preflight-gate.md` | ⭐ STEP 0 前置门禁：声明/验证/拦截三条 MUST NOT |
| `few-shot-examples.md` | ⭐ 少样本：数量黄金比例、质量三要素、相似度排序 |
| `common-mistakes-checklist.md` | ⭐ 常见错误清单：描述/正文/结构/输出/维护五层 |
| `deterministic-scripts.md` | ⭐ 确定性脚本四原则 + 跑两次 diff + 该不该脚本化 |
| `output-contract-templates.md` | ⭐ 输出契约：模板钉 assets/、三种目录语义 |
| `granularity-atomic-workflow.md` | ⭐ 原子 vs 工作流技能 + 重启测试 |
| `output-control.md` | 输出控制三层次与模板 |
| `unity-refactor-skill.md` | ⭐ 重构技能：默认范围=最近改动、八条规则 |
| `frontend-ui-skills.md` | ⭐ 三 agent 前置、反 AI 味表、委托链 |
| `five-starter-skills.md` | ⭐ 五个起步技能完整源码 |
| `systematic-debugging-skill.md` | ⭐ 技能样本：四阶段、三次修复规则、写法分析 |
| `code-review-skill-instance.md` | ⭐ 技能实例：八步、三档判词、三条硬规则 |
| `scripts-as-production.md` | ⭐ 脚本即生产代码：JSON over stdout 契约 |
| `first-skill-minimal.md` | ⭐ 第一个技能可以只有 10 行 + 四条黄金法则 |
| `activation-mechanism.md` | ⭐ 激活机制：纯 LLM 推理，description 是唯一杠杆 |
| `claude-md-bidirectional.md` | ⭐ CLAUDE.md 与技能的双向流动、头号反模式 |
| `infinite-loop-timeout.md` | ⭐ 无限循环与超时：终止条件、每技能单独 timeout |

**指令怎么写**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **形态匹配：禁令 / 配方 / 槽位 / 条件** | `references/guidance-forms.md` |
| **反理性化：agent 找借口跳过步骤** | `references/anti-rationalizations.md` |
| **事实边界：该写什么不该写什么** | `references/fact-boundary.md` |
| **措辞、语气、格式** | **`skill-authoring` 的 `writing-style.md`** |

**结构与组织**：

| 你要做的事 | 读 |
|---|---|
| **写 scripts/ 里的脚本** | `references/script-engineering.md` |
| ⭐ **逐步写失败模式：只有 happy path 会在生产里断** | `references/failure-modes-doc.md` |
| ⭐ **工具输出设计：输出就是推理的原材料** | `references/tool-output-design.md` |
| ⭐ **范围章节：Out of scope 要指向替代方案** | `references/scope-section.md` |
| ⭐ **反模式章节：四要素与具体成本** | `references/anti-pattern-section.md` |
| **长任务的进度报告：按阶段报、降级必须说** | `references/progress-reporting.md` |
| **术语一致性：一个词两个意思就够糟了** | `references/terminology.md` |
| ⭐ **16 条实战原则** | `references/skill-principles.md` |
| ⭐ **官方团队经验：别陈述显而易见、别过度约束** | `references/official-lessons.md` |
| ⭐ **CLAUDE.md / AGENTS.md / SKILL.md 怎么选** | `references/claude-md-vs-skill.md` |
| **指令分层：什么该放 AGENTS.md** | `references/instruction-layering.md` |

**输出与收尾**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **输出契约：Schema-First、四道防线** | `references/output-contract.md` |
| ⭐ **落地与验证：怎么证明"完成了"** | `references/grounding-verification.md` |
| **失败处理、重试、熔断、降级** | `references/error-handling.md` |
| ⭐ **幂等、状态文件、恢复与回滚** | `references/idempotency-resume.md` |
| ⭐ **行动前先查状态** | `references/state-check.md` |

## Critical Rules

**形态**：

- **禁令只在防明知故犯时有效**；形状问题用配方
- 依条件而定的行为写 `if <可观察谓词> then`，不写"视情况而定"
- ❌ **不给规则加"除非""如有需要"**——例外条款会重新打开谈判空间，且无法限定作用域

**验证章节（每个技能必须有）**：

- 写明**具体命令**、什么证据够什么不够
- 禁用"应该 / 看起来 / 我很有信心"
- ⭐ **建造者不能当审计员**——派全新只读子代理复核，agent 默认会"幻觉式合规"
- 校验**分必做与按需**——过度验证是最大单一成本源

**目录与脚本**：

- `scripts/` = 要结果一致（执行，不占上下文）；`references/` = 要每次有新见解（读进上下文）
- 脚本必须**非交互**、JSON 输出、区分退出码、幂等
- `assets/` 的文件不是用来读的，是**被当作输入或模板消费的**
- ⭐ 未被引用的 asset 是噪音——会稀释检索

**分层**：

- 技能可以保持简洁，因为**从 bootstrap 层隐式继承了工作区约定**
- ❌ 把同一份清单同时粘进 AGENTS.md、Cursor rule 和技能——三处必然漂移
- 含"绝不"且机器能检查的规则 → 用 hook，不写进提示词

**执行安全**：

- **任何重试或轮询都必须声明最大次数**——见过跑满 200 次烧光 token 的生产事故
- **删除 / push / 部署必须设人工确认门槛**（先输出命令清单，确认后再执行）
- **不写硬编码密钥 / 内网地址 / 项目专属路径**——只写"从环境变量读取"

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "多写几条禁令更保险" | 禁令只在防明知故犯时有效；形状问题用配方，否则反噬。 |
| "多加几步校验更安全" | 过度验证是最大单一成本源。分必做/按需。 |
| "写灵活一点更好用" | 无具体判据的词对模型等于没有约束，必须给可观察标准。 |
| "脚本直接写在 SKILL.md 里就行" | 确定性逻辑必须进 scripts/——省 token 且结果确定。 |
| "跑一遍扫描器显示 SAFE 就够了" | SAFE ≠ 安全。先确认扫描器实际启用了几个引擎。 |

其余见 `references/anti-rationalizations.md`。

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验（含孤儿资产、引用链套检测）
python scripts/validate_skill.py ./my-skill --strict   # 警告也当错误
python scripts/estimate_tokens.py ./my-skill     # 估算正文与 references 成本
```
