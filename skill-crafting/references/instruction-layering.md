# 指令分层：什么该放哪一层

## 目录

- [五种文件，五种职责](#五种文件五种职责)
- [一条判断规则](#一条判断规则)
- [优先级与冲突裁决](#优先级与冲突裁决)
- [推荐的仓库布局](#推荐的仓库布局)
- [AGENTS.md 是协调层，不是流程层](#agentsmd-是协调层不是流程层)
- [膨胀的 AGENTS.md 怎么拆](#膨胀的-agentsmd-怎么拆)
- [三个反模式](#三个反模式)

---

## 五种文件，五种职责

| 文件 | 谁写 | 性质 | 加载 |
|---|---|---|---|
| **CLAUDE.md** | 你 | Claude 专属行为覆盖 | 会话启动，始终 |
| **AGENTS.md** | 你 | **通用项目法**——架构与约定，所有 agent 都读 | 会话启动，始终 |
| **MEMORY.md** | **agent** | 历史决策与经验 | 按需或始终 |
| **SKILL.md** | 你/团队 | **任务专属专长** | 按需 |
| **CONTEXT.md** | 你 | 当前会话状态 | 会话级 |

**层级关系**：

```
Bootstrap 层（AGENTS.md / CLAUDE.md）
        ↓  建立持久的环境假设
Skill 层（SKILL.md）
        ↓  定义专门流程
Execution 层（具体工具调用与推理）
```

> **这个分层在架构上很重要**：它把隐式的运行时行为
> 变成了**显式的、可检查的、可版本控制的工件**。

**关键收益**：技能可以保持简洁，
因为**它从 bootstrap 层隐式继承了工作区约定**。
同时工作区策略可以独立演进，**不需要重写每一个技能**。

---

## 一条判断规则

> **如果几乎每个任务都需要它 → rules / AGENTS.md**
> **如果只有部分任务需要它 → skill**
> **如果需要实时数据 → MCP，不是更长的规则文件**

| 内容 | 放哪 |
|---|---|
| 技术栈版本、包管理器 | AGENTS.md |
| lint / test / build 命令 | AGENTS.md |
| 命名与文件结构约定 | AGENTS.md |
| **禁止触碰的路径** | AGENTS.md |
| 500 行的安全审查清单 | **Skill** |
| 发布/审计/迁移/事故流程 | **Skill** |
| API 凭据、连接串 | **环境变量 + MCP**，不进任何 md |

**更细的二分**：

```
标准 repo 检查命令        → AGENTS.md
专业多步流程里的一环命令   → Skill
影响日常编码决策的架构规则 → AGENTS.md
```

---

## 优先级与冲突裁决

**权威层级（从高到低）**：

```
1. CLAUDE.md     —— Claude 专属，对 Claude 会话覆盖一切
2. AGENTS.md     —— 通用项目规则
3. SKILL.md      —— 任务专属；技能加载时，其规则在该任务内优先于 AGENTS.md 通用约定
4. CONTEXT.md    —— 会话级现实检查，仅覆盖本会话的假设
5. MEMORY.md     —— 历史参考，是日志不是规则书，不覆盖当前指令
```

**冲突例子**：AGENTS.md 说用单引号，CLAUDE.md 说用双引号 →
**Claude 会话里 CLAUDE.md 赢**；
但 Copilot 读同一个项目只看到 AGENTS.md，用单引号。

> **这个设计的优雅之处**：CLAUDE.md 为 Claude 定制行为，
> **同时不破坏通用标准**。

**Codex 的特殊机制**：`AGENTS.override.md`——
在给定作用域内**先检查 override 文件，再检查普通 AGENTS.md**。
子目录可以用它覆盖局部规则。

**⚠️ 一个易踩的坑**：技能加载目标优先级里，
**SKILL.md 的 `target_agent` 高于 AGENTS.md 的声明**。
若两者不一致，建议团队约定**只用其中一种**，避免配置冲突。

| 团队规模 | 建议 |
|---|---|
| 个人项目 | 直接在 SKILL.md 设 `target_agent` / `category` |
| 小团队 | 在 AGENTS.md 集中管理分配，SKILL.md 只留通用字段 |
| 大团队 | SKILL.md 定义作者意图（`category`），AGENTS.md 定义部署时实际分配 |

---

## 推荐的仓库布局

```
your-repo/
├── AGENTS.md                      # 始终在线的小指令链
├── .agents/skills/                # 跨客户端约定路径
│   ├── release-checklist/
│   │   ├── SKILL.md
│   │   └── references/release-risk-table.md
│   └── security-review/
│       ├── SKILL.md
│       └── scripts/scan_changed_files.sh
├── services/payments/
│   ├── AGENTS.override.md         # 局部覆盖
│   └── .agents/skills/payments-runbook/SKILL.md
└── README.md
```

> **这套布局给 Codex 一个小的始终在线指令链 + 聚焦的按需工作流。**
> 根级技能覆盖通用流程；payments 服务可以覆盖局部规则并定义自己的 runbook。

---

## AGENTS.md 是协调层，不是流程层

> **最好区分 AGENTS.md 和 SKILL.md 的方式，是问各自装什么知识：**
>
> - **SKILL.md 装任务局部流程**：完成一类工作所需的步骤、默认值、检查、资源
> - **AGENTS.md 装工作区级运作策略**：任务怎么路由、输出怎么评审、
>   约定怎么遵守、什么时候该引入别的 agent 或人

**AGENTS.md 该写的（协调，而非执行）**：

```
□ 工作如何在 agent / 阶段之间分解
□ 哪类信息以哪些文件/目录为权威
□ 输出被视为完成前要经过哪些验证或评审门
□ agent 之间如何传递中间状态
□ 什么动作需要升级（escalation）
□ 速度/安全/成本/完备性之间的取舍怎么处理
```

**例子**：一个报告技能描述"产出基准报告的具体步骤"；
AGENTS.md 则规定"本工作区的报告必须引用来源、
保持特定文档结构、通过校验、发布前经评审"。

> ⭐ **这个分离让每个技能都不必重复携带同一套工作区规则**——
> 引用策略、评审要求、升级行为、仓库约定**在 AGENTS.md 里只活一次**。

---

## 膨胀的 AGENTS.md 怎么拆

如果 AGENTS.md 已经变成"团队写过的所有流程的垃圾场"，这样拆而不丢行为：

```
1. 保留在 AGENTS.md：设置、标准检查、架构、编码规则
2. 长流程移到 .agents/skills/<name>/SKILL.md
3. 深度参考材料移到各技能的 references/
4. AGENTS.md 里加一个简短的 "Available Workflows" 段落，点名各技能
5. 每个技能用显式 $skill 调用测一遍，再用自然语言提示测一遍
```

**AGENTS.md 链接技能的写法**：

```markdown
## Standard Checks
- 改应用代码后跑 `pnpm lint`
- 改共享逻辑后跑 `pnpm test`
- 报告跑不了的检查

## Available Workflows
- 发布就绪检查 → 用 `release-checklist` 技能
- 安全敏感改动 → 用 `security-review` 技能
- 数据库迁移 → 用 `migration-review` 技能

## Project Rules
- API 输入校验放在路由处理器附近
- 客户数据不进日志
- 优先复用现有 UI 组件
```

> 这样 AGENTS.md 只有约 50 行，
> **技能把流程深度按需带进来**。

---

## 三个反模式

### ❶ 把每个工作流都塞进 AGENTS.md

> 这让**每个会话都背着可能无关的专业指令**。

✅ 把大型发布、审计、迁移、事故流程移进技能。

### ❷ 把核心仓库规则只放在技能里

> **如果这条规则对大多数编辑都重要，agent 可能在技能激活前就已经错过了它。**

✅ 核心项目预期留在 AGENTS.md。

### ❸ 重复且矛盾的规则

> AGENTS.md 说测试命令是 A，技能里说是 B——agent 得自己裁决冲突。

✅ **AGENTS.md 作为标准检查的真相源，技能反过来引用它。**

> ⚠️ **头号反模式：把同一份安全清单同时粘进 AGENTS.md、Cursor rule 和技能里。**
> 三处必然漂移，而漂移的规则比没有规则更糟。

---

## 自查

```
□ 这条规则是"几乎每个任务都要"还是"只有部分任务要"？
□ 核心仓库规则是否留在 AGENTS.md（而非只在技能里）？
□ 长流程是否已从 AGENTS.md 移进技能？
□ AGENTS.md 是否有 "Available Workflows" 指向各技能？
□ 标准检查命令是否只有一个真相源（AGENTS.md）？
□ 同一份清单有没有被复制到多处？
□ 是否用了 .agents/skills/ 跨客户端约定路径？
□ 子目录需要覆盖时是否用了 AGENTS.override.md？
```
