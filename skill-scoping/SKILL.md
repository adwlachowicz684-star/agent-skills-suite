---
name: skill-scoping
description: 技能的边界界定与内容分层——Out of scope 章节该怎么写（要指向替代方案）、原子技能 vs 工作流技能的粒度、四层沉淀（原则/知识/模板/动作各归其位）、指令分层（什么该放 AGENTS.md 或 CLAUDE.md 而不是技能）、事实边界、失败模式章节、以及 16 条结构性原则。用于技能边界模糊、内容和 CLAUDE.md 重复、不知道该拆成几个技能、范围章节写成了废话。
  Do NOT use for 目录与子目录布局（用 skill-structuring）、句子级措辞与形态（用 skill-crafting）、各章节具体写什么（用 skill-content）、该不该做成技能（用 skill-selection）。
---

# 技能的边界与分层

## 边界

- 用于：**范围章节** · 粒度（原子/工作流）· 四层沉淀 · 指令分层 · 事实边界 · 失败模式章节
- 不用于：目录布局 · 句子级措辞 · 章节内容写法 · 该不该做

## 核心原则

> ⭐ **技能的能力边界不是"它做什么"，而是"它不做什么"——
> 而每一条"不做"都必须指向一个替代方案。**

```
❌ "不处理加密 PDF"
✅ "不处理加密 PDF——先用 decrypt.py 解密，再调用本技能"
```

> ⭐⭐⭐ **没有替代方案的 Out of scope，等于把用户丢在门口。**

四个常见的边界错误：

| 错误 | 表现 |
|---|---|
| 边界太宽 | description 里"或"出现两次以上 |
| 边界太窄 | 一个动作也成一个技能（"读取标题"） |
| ⭐ 边界靠猜 | 没写 Out of scope，全靠模型自己判断 |
| ⭐⭐ 边界重复 | 同一份清单同时粘进 AGENTS.md、Cursor rule 和技能——**三处必然漂移** |

## 何时不用本技能

- 文件放哪个子目录 → `skill-structuring` 的 `directory-contract.md`
- 禁令还是配方、措辞怎么写 → `skill-crafting` 的 `guidance-forms.md`
- 这个任务该不该做成技能 → `skill-selection` 的 `worth-skillifying.md`
- 拆分信号与重构时机 → `skill-refining` 的 `split-signals-five.md`

## 路由表（按需深读）
| `scope-section.md` | ⭐⭐⭐⭐⭐ 范围章节：Out of scope 要指向替代方案；边界四错误 |
| `granularity-atomic-workflow.md` | ⭐⭐⭐⭐ 原子 vs 工作流；⭐ 重启测试判据 |
| `claude-md-bidirectional.md` | ⭐⭐⭐⭐ CLAUDE.md 与技能的双向流动；⭐⭐⭐ 头号反模式 |
| `content-layering-four.md` | ⭐⭐⭐⭐ 四层沉淀：原则/知识/模板/动作各归其位 |
| `instruction-layering.md` | ⭐⭐⭐ 指令分层：什么该放 AGENTS.md 而不是技能 |
| `claude-md-vs-skill.md` | ⭐⭐⭐ CLAUDE.md / AGENTS.md / SKILL.md 怎么选 |
| `fact-boundary.md` | ⭐⭐⭐ 事实边界：技能该写什么、不该写什么 |
| `failure-modes-doc.md` | ⭐⭐⭐⭐ 逐步写失败模式：⭐ 只有 happy path 会在生产里断 |
| `skill-principles.md` | ⭐⭐⭐ 16 条实战原则 |
| `official-lessons.md` | ⭐⭐⭐ 官方团队经验：别陈述显而易见、别过度约束 |

**划边界**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 写 Out of scope 章节 | `scope-section.md` |
| 事实与指导怎么分 | `fact-boundary.md` |
| ⭐ 只有正向流程够不够 | `failure-modes-doc.md`（不够） |

**定粒度**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 原子还是工作流 | `granularity-atomic-workflow.md`（含重启测试） |
| 内容分几层 | `content-layering-four.md` |

**与全局文件分工**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 放技能还是 CLAUDE.md | `claude-md-vs-skill.md` · `claude-md-bidirectional.md` |
| 放技能还是 AGENTS.md | `instruction-layering.md` |

## Critical Rules

- ⭐ **Out of scope 必须配替代方案**——只说"不做"等于把人丢在门口
- ⭐⭐ **同一份清单不得重复出现在 AGENTS.md、Cursor rule 和技能里**——三处必然漂移
- 技能可以保持简洁，因为**从 bootstrap 层隐式继承了工作区约定**
- ⭐ **边界太窄和太宽一样错**：一个"读取标题"不是技能；"或"出现两次以上多半是两个技能
- ⭐ 失败模式要**逐步写**，不是只写 happy path
- 含"绝不"且机器能检查的规则 → 用 hook，不写进提示词

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "边界写宽点，用不上就不触发" | ⭐ "或"出现两次以上 = 两个技能。宽边界直接稀释触发准确率。 |
| "多写几条"不做"显得严谨" | 没有替代方案的"不做"是把用户丢在门口。 |
| "清单放在三处，总有一处被看到" | ⭐⭐ 三处必然漂移，而漂移后你不知道哪份是真的。 |
| "happy path 写清楚就够了" | ⭐ 只有 happy path 的技能会在生产里断，且断得毫无声息。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 自举校验：结构、路由表覆盖、孤立文件、行数上限 |
| `scripts/estimate_tokens.py <dir>` | 估算正文与 references 成本 |

## 参考

- 相关技能：《skill-crafting》（句子级措辞）·《skill-content》（章节内容）·
  《skill-selection》（该不该做）·《skill-refining》（拆分信号）
