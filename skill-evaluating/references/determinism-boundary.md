# 确定性边界：什么必须放 Hook，什么放技能

> 相关：《skill-selection》的 `five-layer-choice.md` ·
> 《skill-orchestration》的 `skill-vs-subagent.md`

---

## 目录

- [1. ⭐ 只有 Hook 是确定性的](#1--只有-hook-是确定性的)
- [2. ⭐ 决策流程：按顺序问，第一个"是"就定了](#2--决策流程按顺序问第一个是就定了)
- [3. ⭐ 两条反模式](#3--两条反模式)
- [4. 六层横向对比](#4-六层横向对比)
- [5. 组合时的不同规则](#5-组合时的不同规则)

---

## 1. ⭐ 只有 Hook 是确定性的

> ⭐ **只有 hooks 和 settings 是确定性的。**
> **CLAUDE.md 指令、技能内容、子代理提示都是模型读到并"尝试"遵循的上下文——
> 官方文档明确说它们是 "context, not enforced configuration"。**

> ⭐ **如果一条规则必须每次都成立，
> 它属于 hook 或 permissions.deny 规则，而不是散文。**

**最锋利的对比**：

```
CLAUDE.md 里写 "never edit .env"   → ⭐ 是一个请求
PreToolUse hook 拒绝这次编辑        → ⭐ 是强制执行
```

**18 个生命周期事件**：

```
PreToolUse · PostToolUse · UserPromptSubmit · SessionStart
SubagentStop · PreCompact · ……（约二十来个）
```

Hook 可以跑 bash 命令、HTTP 调用、提示、agent，甚至 MCP 工具。
用途：**执行策略、审计日志、注入始终该在场的上下文、
在不信任模型的前提下重定向或阻断它**。

---

## 2. ⭐ 决策流程：按顺序问，第一个"是"就定了

```
Q1 ⭐ 必须每次都发生（或被阻断）、确定性？
    是 → ⭐ Hook（动态逻辑）或 permission 规则（静态 allow/deny）

Q2 是否把 Claude 连到外部系统？
    是 → MCP
    ⭐ 反过来：本地 CLI 用 Bash 就能做得很好的，MCP 是过度设计

Q3 是不是每个会话都需要的"事实或规则"？
    是 → CLAUDE.md
    ⭐ 只适用于部分代码库 → 用 .claude/rules/ 的路径规则

Q4 是不是按需知识或可重复流程？
    是 → ⭐ Skills
        部署清单、API 风格指南、发布工作流、调试手册

Q5 需要隔离的上下文或并行工作者？
    是 → Subagents
```

> ⭐ **顺序很重要**：
> 把只有某一层能满足的约束（确定性、外部连接）**放在最前面**——
> 这样"较软的偏好"就不会从唯一能保证它的那一层手里抢走工作。

---

## 3. ⭐ 两条反模式

**① 把编码规范放进 Hook 的 SessionStart 注入**

```
⭐ 看起来聪明一周，
⭐ 然后当这条规范需要"根据正在编辑的文件"而变条件时就崩了
⭐ ——技能原生就能处理这个
```

**② 把破坏性命令拦截写进技能**

> ⭐ **这是表演。**
> 模型会加载技能、确认这条指令，
> **然后三轮后当它要写测试时把它忽略掉。**

> ⭐ 一句话总结：
> **Hooks 用于模型不可被信任去遵守的事；
> Skills 用于模型需要知道的事。**

---

## 4. 六层横向对比

| 维度 | Skills | Subagents | Plugins | Hooks |
|---|---|---|---|---|
| 存放位置 | `.claude/skills/<name>/SKILL.md` | `.claude/agents/*.md` | `~/.claude/plugins/` | `settings.json` 的 hooks 键 |
| 激活方式 | **description 匹配对话** | Task 工具显式调用 | 用户 `/plugin install` | ⭐ **生命周期事件触发** |
| 作用域 | 程序性知识 | 隔离上下文做旁路任务 | 其他原语的分发包 | 确定性策略 / 可观测性 |
| 可组合性 | 载入主或子代理上下文 | 可用任何工具 + 加载技能 | 一起打包技能/子代理/Hooks/MCP | 绕着任何工具跑 |
| 最适合 | ⭐ **自动激活的教学程序** | 并行化或隔离噪声工作 | ⭐ **把团队整套栈一次装好** | ⭐ **执行模型无法选择退出的策略** |
| 信任边界 | 可信代码路径 | 沙箱上下文 | 安装时可信，采用前要审计 | ⭐ **以用户身份运行，完整文件系统访问** |
| 跨端可移植 | ⭐ **强** | 弱（Claude Code 专属） | 弱 | 弱 |

**三条结论**：

```
① ⭐ 只有 Hooks 确定性触发——其他每个原语都依赖模型决定要不要用
② ⭐ 只有 Plugins 负责分发——团队要同一套配置，Plugins 是载体，其他是货物
③ ⭐ Skills 跨 agent 可移植性最强（open agentskills 规范）
   ——写一次，Cursor/Codex/Cline/Gemini CLI 都能读
```

> ⭐ **如果跨编辑器可移植性对你重要：
> 优先靠 Skills，把其余当作 Claude Code 本地的胶水。**

---

## 5. 组合时的不同规则

不同层在多级定义时，组合方式**不一样**——这点极易搞错：

| 层 | 组合方式 |
|---|---|
| CLAUDE.md | ⭐ **叠加**——所有层级同时加载并拼接 |
| Skills / Subagents | ⭐ **按名覆盖**——高优先级作用域赢 |
| MCP servers | 按名覆盖，local 优先于 project，再是 user |
| ⭐ Hooks | ⭐ **合并**——每个已注册的 hook 都会为其事件触发，**不论来源** |
| Settings | 优先级链：managed > CLI > local > project > user |

> ⭐ **Hooks 是"合并"这条最反直觉**：
> 你装了两个 hook，不是后一个覆盖前一个，**是每个都会跑**。

**一个具体例子**（团队要三件事）：

```
每个迁移文件必须含 DOWN  → ⭐ Hook（PreToolUse on Write）
                          非协商，必须 100% 触发，模型无法跳过
"review this migration"  → Skill
                          按需程序，只在调用时加载
"所有 SQL 用 snake_case" → ⭐ .claude/rules/db.md + glob db/migrations/**
                          路径规则，只在碰迁移文件时加载
schema registry 查询      → MCP server
```

---

## 速查

```
□ ⭐ 必须每次成立 → Hook / permission.deny，不是散文
□ ⭐ 编码规范放 Hook 的 SessionStart → 会崩（条件化时）
□ ⭐ 破坏性拦截写技能 → 是表演（三轮后就忽略）
□ ⭐ Hooks = 模型不可信的事；Skills = 模型需要知道的事
□ ⭐ Q1-Q5 按顺序问，第一个"是"就定层
□ ⭐ Hooks 是合并不是覆盖（每个都会跑）
□ ⭐ CLAUDE.md 是叠加；技能是按名覆盖
□ ⭐ 跨端可移植 → 优先 Skills
□ 只有 Plugins 负责分发
```

**一句话**：

> ⭐ **"永不编辑 .env"写在 CLAUDE.md 里是一个请求；
> 一个拒绝该编辑的 PreToolUse hook 才是强制执行。**
