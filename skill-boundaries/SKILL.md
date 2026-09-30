---
name: skill-boundaries
description: 技能与其他机制的边界划分——技能 vs RAG vs 微调 vs MCP vs 子代理 vs 工作流引擎 vs 自定义指令，以及五层选型（Prompt/Skill/Project/MCP/Subagent）、能力原语 vs 流程原语、什么时候不该做成技能、领域分类法与行业落地模式。用于回答"这件事该用哪种机制承载"。
  Do NOT use for 库的规模与装载取舍、成本归账、缓存与运行时性能（用 skill-selection）、多技能如何编排（用 skill-orchestration）、技能的具体写法（用 skill-authoring）。
---

# 机制边界：该用哪种机制承载

## 边界

- 用于：**机制对比** · **五层选型** · **该不该做成技能** · **能力原语 vs 流程原语**
- 不用于：库规模与成本 · 多技能编排 · 具体写法

## 核心原则

> ⭐ **四种机制的定位**：
> **Tools 是手，Skills 是脑，RAG 是记忆，微调是本能。**

```
□ ⭐ 想补领域知识 → RAG / references 检索
□ ⭐ 想稳定行动方式 → 技能
   （实测：技能 65.7% 的作用是流程锚定，只有 4.5% 是显性知识注入）
□ 想改变本能反应 → 微调（⭐ 最后手段）
□ 想连接外部系统 → MCP
```

> ⭐⭐⭐ **这条是全部对比的地基**：
> **技能稳定的是"行动方式"，不是"知识"。**
> 想靠技能补知识，多半该用 RAG。

## 何时不用本技能

- 库多大、装几个、成本怎么算 → `skill-selection`
- 多个技能怎么配合 → `skill-orchestration`

## 路由表（按需深读）
| `skill-boundaries/references/skill-vs-mcp-two-layers.md` | ⭐⭐⭐⭐ 失败不对称（隐形 vs 报错）；Token 不对称；编排+执行 |
| `skill-boundaries/references/four-way-choice.md` | ⭐⭐⭐ 四选一：⭐ 三种规则差别只在**何时加载 + 多大范围**；技能=共享 子代理=隔离 |
| `skill-boundaries/references/skill-vs-subagent-decide.md` | ⭐⭐⭐⭐⭐ 判断轴是隔离不是大小；⭐⭐ 子代理挂技能 |
| `skill-boundaries/references/skill-vs-workflow.md` | ⭐⭐⭐ Skill 管怎么做 / Workflow 管流转；⭐⭐⭐ 顺序必须强制就用 Workflow |
| `skill-boundaries/references/skill-vs-workflow-engine.md` | ⭐⭐⭐ 五问判据与迁移信号 |
| `skill-boundaries/references/mcp-vs-skill-decision.md` | ⭐⭐⭐ MCP vs 技能：五问决策法 |
| `skill-boundaries/references/when-not-skill.md` | ⭐⭐⭐ 什么时候不该做成技能 |
| `skill-boundaries/references/when-not-to-use-skill.md` | ⭐⭐⭐ 六条不该做成技能 + ⭐⭐⭐ 伪稳定最危险 |
| `skill-boundaries/references/worth-skillifying.md` | ⭐⭐⭐ 该不该做：三条硬标准 + 五维矩阵 |
| `skill-boundaries/references/capability-vs-process.md` | ⭐⭐⭐ 能力原语 vs 流程原语：做成哪一类技能 |
| `skill-boundaries/references/five-layer-choice.md` | ⭐⭐⭐ 五层选型：Prompt/Skill/Project/MCP/Subagent |
| `skill-boundaries/references/skill-vs-rag.md` | ⭐⭐ 技能 vs RAG：过程性 vs 事实性知识 |
| `skill-boundaries/references/skill-vs-finetuning.md` | ⭐⭐ 技能 vs 微调：诊断差距的顺序 |
| `skill-boundaries/references/instructions-vs-skills-mcp.md` | ⭐⭐ 自定义指令 / 技能 / MCP 怎么选 |
| `skill-boundaries/references/domain-taxonomy.md` | ⭐⭐ 领域分类法：754 技能的检索算术 |
| `skill-boundaries/references/industry-patterns.md` | ⭐⭐ 垂直行业落地模式、五条铁律 |

**按问题查**：

| 你的问题 | 读 |
|---|---|
| ⭐ **补知识还是稳动作？** | `skill-boundaries/references/skill-vs-rag.md` |
| ⭐ **要不要微调？** | `skill-boundaries/references/skill-vs-finetuning.md` |
| ⭐ **用 MCP 还是技能？** | `skill-boundaries/references/mcp-vs-skill-decision.md` · `skill-boundaries/references/skill-vs-mcp-two-layers.md` |
| ⭐ **用子代理还是技能？** | `skill-boundaries/references/skill-vs-subagent-decide.md` |
| ⭐ **顺序必须强制怎么办？** | `skill-boundaries/references/skill-vs-workflow.md` |
| ⭐ **CLAUDE.md / AGENTS.md / SKILL.md？** | **`skill-crafting` 的 `skill-scoping/references/claude-md-vs-skill.md`** |

## Critical Rules

- ⭐ 诊断差距的顺序：**推理不够 → 换模型；知识缺口 → 改检索；格式问题 → 改提示词或轻量微调**
- ❌ **别把"知识缺口"误当成"需要微调"**
- ⭐⭐⭐ **技能没有强制力**——顺序必须强制就用工作流或脚本（同一原则：确定性判断要用确定性机制）
- ⭐⭐⭐⭐ **子代理的判断轴是隔离，不是大小**——把需要上下文的大任务丢给子代理，答案反而变差
- ⭐ 明确 schema 下 GPT ~95% vs Llama 70B ~70%——**25 个百分点的可靠性鸿沟**
- ⭐ 音频 32 tokens/秒（1 小时 ≈ 115K tokens，**比整个技能库还大**）——先算再用

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "做成技能吧，反正都要写文档" | 事实性知识用 RAG 更有效；技能稳定的是行动方式。 |
| "微调一下效果更彻底" | 先诊断差距类型。格式问题不需要微调。 |
| "多模态技能先做起来" | 先算上下文成本——一小时音频比整个技能库还大。 |
| "任务很大，用子代理" | ⭐ 判断轴是隔离不是大小。需要上下文的任务会变差。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 校验 |
| `scripts/estimate_tokens.py <dir>` | 估算上下文成本 |

## 参考

- 相关技能：《skill-selection》（规模与成本）·《skill-orchestration》（多技能编排）·
  《skill-authoring》（具体写法）
