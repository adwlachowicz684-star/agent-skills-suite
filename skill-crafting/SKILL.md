---
name: skill-crafting
description: 打磨 Agent Skill 的正文构件——指令形态、目录契约、脚本工程、输出契约、验证章节、错误处理、指令分层。用于禁令不管用、输出形状不稳、agent 跳步、脚本该不该抽、内容该放 SKILL.md 还是 AGENTS.md、怎么证明"完成了"。
  Do NOT use for 从零创建技能的整体流程（用 skill-authoring）、范围章节与粒度分层（用 skill-scoping）、已有技能的瘦身拆分（用 skill-refining）、评估与打分（用 skill-evaluating），也不用于写一次性提示词。
---

# 技能

> ⭐ **示例与判断依据不在本技能** → 《skill-examples》
> 本技能管「措辞与文体」，那份管「示例怎么来、判断依据怎么写」。正文的构件

## 边界

- 用于：**指令措辞与形态** · 示例设计 · 验收与判断分支 · 整体写法原则与自查
- 不用于：整体创建流程 · 瘦身拆分 · 评估打分 · 一次性提示词
- ⭐ **范围章节、粒度、四层沉淀、与 CLAUDE.md/AGENTS.md 的分工 → 《skill-scoping》**

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
| `vague-word-blacklist.md` | ⭐⭐⭐⭐⭐ 含糊词替换表；⭐⭐⭐⭐⭐ 五类伪装成约束的词（确保/重要：/总是）；可 grep 的 CI 检查 |
| `system-prompt-structure.md` | ⭐⭐⭐ 结构优于长度+五分节；★★★禁令仲裁（第四个来源） |
| `minimum-viable-three-principles.md` | ⭐⭐⭐ 最小可用三原则：★执行契约非产品文档、路径不硬编码 |
| `eight-practical-lessons.md` | ⭐⭐⭐⭐ 八条实战技巧；★给约束不给流程，顺序重要则写脚本 |
| `skill-review-checklist-ten.md` | ⭐⭐⭐ 十条检查清单；★每条规则都要能对应一个失败场景 |
| `conditional-branch-writing.md` | ⭐⭐⭐⭐⭐ 没有 else 的 if = 授权模型自己定义 else；⭐⭐⭐⭐⭐ 半写的约束比不写更危险；⭐⭐⭐⭐⭐ "有但不可用"那档 |
| `list-item-relations.md` | ⭐⭐⭐⭐⭐ 列表项之间是且/或/顺序；⭐⭐⭐⭐⭐ 默认解读是且+顺序；⭐⭐⭐⭐⭐ 混合列表 |
| `unjustified-numbers.md` | ⭐⭐⭐⭐⭐ 没有出处的数字；⭐⭐⭐⭐⭐ 具体性≠有依据；⭐⭐⭐⭐⭐ 数字+出处+越界动作 |
| `skill-readability-layout.md` | ⭐⭐⭐⭐⭐ 两类读者；结构性冗余保留/解释性冗余删除；⭐⭐⭐⭐ 可 diff 性（一个从句一行）；⭐⭐⭐⭐ 每 30 行一小标题
| `writing-style-rfc2119.md` | ⭐ RFC 2119 关键词 + 语义换行 + 20 词上限 |
| `token-bloat-audit.md` | ⭐ 瘦六个动作：合并工具调用、/compact、抑制冗长输出 |
| `write-reasons-not-rules.md` | ⭐ 写原因而非堆规则 + 三成原则 + 风险三档 |
| `imperative-style.md` | ⭐ 祈使句 vs 第二人称 + 尺寸分级 + 评分权重 |

**看完整样本**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **照着一份真技能写 / 看取舍是怎么做的** | **`skill-gallery`**（完整源码 + 写法分析） |
| ⭐ **范围章节、粒度、分层** | **`skill-scoping`** |

**指令怎么写**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **形态匹配：禁令 / 配方 / 槽位 / 条件** | `references/guidance-forms.md` |
| **反理性化：agent 找借口跳过步骤** | **`skill-execution` 的 `anti-rationalizations.md`** |
| **事实边界：该写什么不该写什么** | **`skill-scoping` 的 `fact-boundary.md`** |
| **措辞、语气、格式** | **`skill-content` 的 `writing-style.md`** |

**输出与收尾**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **输出契约：Schema-First、四道防线** | **`skill-execution` 的 `output-contract.md`** |
| ⭐ **落地与验证：怎么证明"完成了"** | **`skill-execution` 的 `grounding-verification.md`** |
| **失败处理、重试、熔断、降级** | **`skill-execution` 的 `error-handling.md`** |
| ⭐ **幂等、状态文件、恢复与回滚** | **`skill-execution` 的 `idempotency-resume.md`** |
| ⭐ **行动前先查状态** | **`skill-execution` 的 `state-check.md`** |

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

**脚本**：

- ⭐ **确定性逻辑必须进 `scripts/`**——写进 SKILL.md 既占上下文又结果不定

**分层**：

- ⭐ 与 CLAUDE.md / AGENTS.md 的分工见 **`skill-scoping`**
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
| "跑一遍扫描器显示 SAFE 就够了" | SAFE ≠ 安全。先确认扫描器实际启用了几个引擎。 |

其余见 **`skill-execution`** 的 `anti-rationalizations.md`。

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验（含孤儿资产、引用链套检测）
python scripts/validate_skill.py ./my-skill --strict   # 警告也当错误
python scripts/estimate_tokens.py ./my-skill     # 估算正文与 references 成本
```
