---
name: skill-orchestration
description: 多个 Agent Skills 与子代理的编排协作。用于设计多技能流水线（串行/并行/条件/循环/嵌套）、决定该用技能还是子代理、处理技能间冲突与重叠、配 MCP 与技能的协作、跨会话记忆与长任务续接、多角色审查编排，或用 Hooks / 定时任务让技能自动跑。
  Do NOT use for 单个技能的写法与打磨（用 skill-authoring / skill-crafting）、瘦身拆分（用 skill-refining）、发布推广（用 skill-distribution），也不用于一般性的多智能体理论讨论。
---

# 多技能与子代理编排

## 边界

- 用于：**多技能流水线** · **技能 vs 子代理** · **冲突与重叠** · **MCP 协作** · **记忆续接** · **自动化触发**
- 不用于：单技能写法 · 瘦身拆分 · 发布推广 · 泛泛的多智能体理论

## 核心原则

> ⭐ **Skill 是应用程序装在主机里；SubAgent 是虚拟机跑完交回结果。**

**两步决策法**：

```
1. ⭐ 要不要"记住这个过程"？
   要 → Skill；只要结果 → SubAgent
2. ⭐ 要不要并行 / 隔离 / 特殊权限？
   要 → SubAgent；都差不多 → 只写 Skill
```

> ⭐ **别为了"酷炫"和"概念完整"而过度设计**——
> 一个技能能解决的事不要拆成一堆子代理。

> ⭐ **组合的甜蜜点是 5–8 个**。超过之后收益递减。

## 路由表（按需深读）
| `skill-dependency-injection.md` | ⭐⭐ 依赖注入四模式：委托/链式/配置/共享服务；双向无知=解耦证据 |
| `orchestrator-timing.md` | ⭐⭐⭐ 过早编排=过早抽象；手动搬运>3次才写编排器 |
| `composition-patterns-types.md` | ⭐ 四种依赖类型 + 隐式依赖等三个组合反模式 |
| `skill-chaining-composition.md` | ⭐ 串联组合：叠加加载、交接协议、五个坑 |
| `context-isolation-fork.md` | ⭐ 上下文隔离：三条件才 fork + 六种别 fork |
| `collision-arbitration.md` | ⭐ 技能打架仲裁三招 + 两步路由 + 延迟真相 |
| `state-persistence.md` | ⭐ 会话间状态持久化：三类状态与读写时机 |
| `gamedev-skill-routing.md` | ⭐ 多维技能库路由：三维正交、指纹识别、降级 |
| `subagent-skill-inheritance.md` | ⭐ 子代理不继承技能，内置 agent 完全用不了 |
| `subagent-teams.md` | 子代理团队：依赖分析→并行批次→关卡 |
| `skills-mcp-subagent.md` | 技能/MCP/子代理协同范式与治理先行 |
| `skill-subagent-combo.md` | ⭐ Skill × 子代理：两个方向、三种模式 |

**编排模式**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **五种编排模式（串行/并行/条件/循环/嵌套）** | `references/composition.md` |
| ⭐ **组合模式、冲突三解法、数量控制** | `references/skill-composition-patterns.md` |
| **子代理配合、不继承技能** | `references/subagents.md` |
| ⭐ **子代理进阶：不能嵌套、可恢复、transcript 独立** | `references/subagent-advanced.md` |
| **该用技能还是子代理** | `references/skill-vs-subagent.md` |
| ⭐ **多角色审查：challenge_agent 是必需角色** | `references/multi-agent-review.md` |
| ⭐ **技能动态激活与停用** | `references/skill-activation.md` |
| ⭐ **多 Agent 并行流水线 / 反幻觉验证** | `references/security-pipeline.md` |
| ⭐ **并行子代理：五种模式与四个坑** | `references/parallel-subagents.md` |
| ⭐ **交接协议：阶段之间传什么** | `references/handoff-protocol.md` |
| ⭐ **Fan-out / Fan-in：难点在汇聚不在并行** | `references/fan-out-fan-in.md` |
| ⭐ **可组合模式：管道/扇出/装饰器/回退/过滤 + 调用链** | `references/composable-patterns.md` |
| ⭐ **Fork 上下文技能：把大 diff 隔离到子代理** | `references/fork-context-skill.md` |
| ⭐ **Fork 官方细则：background、rewind、返回空** | `references/fork-official-details.md` |
| ⭐ **技能 vs 斜杠命令：100% 触发 vs 按需** | `references/skill-vs-command.md` |
| ⭐ **步数/时间/花费上限：三个维度都要且 fail closed** | `references/spend-limits.md` |

**与外部系统协作**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **Skill × MCP：三层栈与三种混合模式** | `references/mcp-composition.md` |
| ⭐ **MCP 协同落地：配置、护栏、四个坑** | `references/mcp-integration-patterns.md` |
| ⭐ **命名空间冲突：互斥点名、遮蔽、参数冲突** | `references/namespace-collision.md` |
| **技能 / MCP / A2A 三层分层** | `references/protocol-layering.md` |

**状态与自动化**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **跨会话记忆、交接班协议** | `references/memory-state.md` |
| ⭐ **持久化产物：CONTEXT.md / ADR / 决策日志** | `references/cross-session-artifacts.md` |
| ⭐ **记忆分层：四层写入节奏、遗忘是特性** | `references/memory-tiers.md` |
| **Hooks / 定时任务 / 技能的分工** | `references/automation.md` |
| ⭐ **提示注入：技能本身是注入通道** | `references/prompt-injection.md` |
| ⭐ **升级规则：把"有疑问就问人"写成可判定条件** | `references/escalation-rules.md` |

## Critical Rules

- ⭐ **子代理不从父对话继承技能**——必须在 `skills:` 显式声明；编排总是一层深
- ⭐ **每个团队都必须包含一个 `challenge_agent`**——专家专注自己领域**会漏掉横切关注点**
- ⭐ **分歧时不要投票**——回到需求、测试与真实运行条件；**分歧本身是信息**
- **汇总规则比分工更重要**——没有汇总规则，主任务只收到几份互相独立的长报告
- 并行组合的前提是**各技能输出互不依赖**，汇总时才需要契约
- 超时 **90 秒**；分支条件必须**可执行**（不能写"视情况"）
- ⭐ **重叠要么定优先级，要么合并，要么限定作用域**——不能放着不管
- 冲突信号：agent 犹豫 · 产出前后不一致 · 出现 lint/类型错误 · 答案飘
- ⭐ **方法 3（限定作用域）最优雅**——它让冲突根本不发生
- 多角色编排必须明确**"谁能改盘、谁只能提议"**，否则会并发改同一文件

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "多拆几个子代理显得更专业" | 一个技能能解决的事别拆。别过度设计。 |
| "子代理会自动继承我的技能" | ❌ 不会。必须在 skills: 显式声明。 |
| "两个技能有点重叠，先放着" | 重叠会稀释检索并让路由摇摆。定优先级或合并。 |
| "并行跑更快，不检查依赖" | 有依赖的并行会产出互相矛盾的结果。 |
| "投票决定分歧" | 分歧是信息。回到需求与测试，不要投票。 |
| "角色越多覆盖越全" | 角色越多，编排与权限越像小型工作流引擎。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验单个技能
python scripts/estimate_tokens.py ./my-skill     # 估算组合后的上下文占用
```
