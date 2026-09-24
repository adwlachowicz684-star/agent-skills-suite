# CLAUDE.md vs AGENTS.md vs SKILL.md：什么放哪里

> ⭐ **一句话判据**：
> **如果 agent 在每个任务上都需要知道它 → CLAUDE.md；
> 如果它只对一类任务重要 → Skill；
> 如果它必须被强制执行 → 权限、沙箱、hooks 或策略，而不是 Markdown。**

## 目录

- [四个去处，四种成本模型](#四个去处四种成本模型)
- [一句话测试（四选一）](#一句话测试四选一)
- [三层对照表](#三层对照表)
- [为什么默认答案是"不放 CLAUDE.md"](#为什么默认答案是不放-claudemd)
- [迁移：把 CLAUDE.md 的某节搬进技能](#迁移把-claudemd-的某节搬进技能)
- [三层组织与软链](#三层组织与软链)

---

## 四个去处，四种成本模型

| 去处 | 加载时机 | token 成本 | 强制力 |
|---|---|---|---|
| **CLAUDE.md** | 每个会话自动 | ⭐ **每次请求都付** | 建议性 |
| **.claude/rules/** | 每会话，或读到匹配文件时 | 带 `paths:` 时按需 | 建议性 |
| **Skill 正文** | 任务匹配时（或 `/` 显式调用） | 按需 | 建议性，但有作用域 |
| ⭐ **Hook** | 从不以散文形式进入上下文 | ⭐ **约等于零** | ⭐ **确定性** |
| **docs/** | agent 被指向时才读 | 按需 | 无（纯参考） |

> ⭐ **Hook 是唯一"零 token + 确定性"的位置**——
> 呼应 `skill-orchestration` 的 `automation.md` 与 `instruction-layering.md`：
> **别让语言模型记住 shell 脚本能强制的事。**

---

## 一句话测试（四选一）

> ⭐ **这是最实用的一套判据，一句一个去处**：

```
留在 CLAUDE.md
  如果它"每一轮都为真、陈述成本低、违反代价高"
  → 构建命令、命名约定、"test/ 按路径镜像"、提交语气
  → ⭐ 判据：即使在一场不相关的重构中途，
     你也希望这条规则生效 → 它就是不变量

移到 Skill
  如果它以"当做 X 时"开头
  → 部署清单、评审 rubric、发布说明格式、迁移 playbook
  → ⭐ name 与 description 始终可见（可发现），
     正文只在任务真正匹配时才加载——
     ⭐ 正是你要的"可发现但不按次计费"

移到 Hook
  如果这句话含"绝不"或"总是"，且机器能检查
  → 提交前格式化、受保护路径、"不许碰 .env"、禁止 push 到 main
  → ⭐ 无论上下文是新的还是陷在五十个文件里，hook 都确定性触发

移到 docs/
  如果它是"agent 应该读"而不是"agent 应该遵守"的东西
  → 架构总览、API 怪癖、计费模块为什么长这样
  → 在 CLAUDE.md 里留一行说明何时读它
```

---

## 三层对照表

| 维度 | CLAUDE.md | .claude/rules/ | Skill |
|---|---|---|---|
| **加载** | 每会话自动 | 每会话，或按 `paths:` 匹配 | ⭐ 按需（调用或相关时） |
| **能否 `@` 引入** | 可以 | 可以 | 可以 |
| **能否触发工作流** | 否 | 否 | ⭐ 可以（`/`） |
| **适合** | 核心约定与构建命令 | 语言/目录专属指南 | 参考资料、可重复工作流 |

**规模建议**（官方口径）：

```
□ ⭐ CLAUDE.md 保持在 200 行以内
   官方原话："target under 200 lines per CLAUDE.md file.
             Longer files consume more context and reduce adherence."
□ 超了就衰减——agent 会忽略后半部分，
   或在不相关的上下文里过度应用某条规则
```

> ⭐ 这条最初是社区经验（HumanLayer），**后来被官方写进了文档**，
> 措辞几乎一致。所以它不再是建议，是尺子。

**AGENTS.md 与 CLAUDE.md 的关系**：

```
□ AGENTS.md 是开放的项目指令格式，跨 agent 共享（Codex 等）
□ ⭐ 官方直白："Claude Code reads CLAUDE.md, not AGENTS.md"
□ 推荐做法：建一个 CLAUDE.md 去 import 它
   # CLAUDE.md
   本项目的通用编码规则见 @AGENTS.md
   支付模块专项规则见 @.claude/skills/pay-ini-key/SKILL.md
□ 或者更省事：ln -s AGENTS.md CLAUDE.md
   ⚠️ Windows 建软链需管理员权限或开发者模式
      → 跨平台协作用 @AGENTS.md 导入更稳
□ ⭐ 不要两边都写完整内容——那必然漂移
```

---

## 为什么默认答案是"不放 CLAUDE.md"

> ⭐ **常驻路径上叠加了三重成本**：

```
① ⭐ 每次请求都付
   4000 token 的 CLAUDE.md = 每次 prompt、
   每次工具往返都付 4000 token，一整天
   实测：把只在发布日才用得上的那一半挪出去，
        每个请求的开销立降，且什么都没坏

② ⭐ 注意力被稀释
   20 条规则，每条只分到一小片"合规预算"
   5 条规则，每条才有真实分量
   → 精简的文件守得住，臃肿的会被当成建议抽样

③ ⭐ 长会话会侵蚀散文
   上下文被 diff 和工具输出填满后，早期指令会淡出
   压缩之后存活的是摘要，⭐ 不是你的原话
```

```
Hook   规避全部三条
Skill  规避前两条
docs/  三条都规避，但完全不强制
⭐ CLAUDE.md 是唯一付全价的位置——把它花在少数配得上的规则上
```

**一份精简 CLAUDE.md 长什么样**：

```markdown
# myproject — agent guide

## Commands
- Build: `pnpm build` / Test: `pnpm test`
- ⭐ Never run `pnpm deploy` directly — use the deploy skill.

## Conventions (always)
- TypeScript strict; ...
```

> ⭐ 注意 `Never run ... — use the deploy skill` 这种写法：
> **禁令 + 明确指向替代方案**，呼应 `guidance-forms.md` 的
> "NOT for X → 用 Y 代替"是最强路由提示。

---

## 迁移：把 CLAUDE.md 的某节搬进技能

**迁移四步**（可直接照做）：

```
1. 把那一节抽到 ~/.claude/skills/<name>/SKILL.md
2. ⭐ frontmatter 的 description 保持紧凑
   "Use when the user wants to wrap up a session..."
3. 正文保留原来的 schema、rules、examples
4. ⭐ 在 CLAUDE.md 里用一行替换原来的 60 行：
   "Session ending: invoke /handoff. Schema and format rules in the skill."
```

```
结果：CLAUDE.md 每个会话短了 60 行
      规则仍然被编码着
      ⭐ 相关 context 在相关时加载；其他时候 dead weight 消失
```

> ⭐ **上下文文件应该引用技能，而不是内联技能**——
> "schema 变更请用 db-migration 技能"这一行几乎不花钱，
> 却能把 agent 路由到正确的流程。
> 把流程粘进 CLAUDE.md，则是**每个任务永远付钱**。

**什么时候技能是错误选择**（三种情况应留在 CLAUDE.md）：

```
□ ⭐ 规则每个会话都适用
   如果 agent 在做任何决定前都需要知道它 → 必须在 CLAUDE.md
   硬流程规则与项目定位是典型
□ 规则很短
□ 规则是"决不"且已被 hook 覆盖（那就不需要任何一处）
```

---

## 三层组织与软链

**两层技能组织**：

```
用户级  ~/.claude/skills/      所有项目加载
        个人编码风格 · 通用输出偏好 · 跨语言基本功

项目级  .claude/skills/        仅当前项目加载
        领域模型术语 · 特定框架用法 · 项目专属的枚举与基类约束

⭐ 同名时项目级优先
⭐ 规则很简单：通用的往上提，专属的下沉
```

**一个真实的归属判断例子**（四条 Java 规则）：

| 规则 | 归属 | 理由 |
|---|---|---|
| 交互提示用中文 | 用户级 | 个人偏好，跨项目一致 |
| 行尾不留空格 | 用户级 | 通用编码卫生 |
| Java 内部调用加 `this.` | 用户级/项目级 | 看是个人偏好还是团队约定 |
| ⭐ 支付 ini key 放 `PayConfEnum` | **项目级** | ⭐ 只对 order-svc 有意义 |

> ⭐ 第四条归项目级的理由很关键：
> **其他项目的 agent 根本不会知道有这么个枚举，也就不会瞎套用。**

**跨工具的事实**（`SKILL.md` 的相对优势）：

```
□ 一个仓库曾要维护三份竞争指令文件（CLAUDE.md / AGENTS.md / .cursorrules）
  且彼此无共享工具
□ ⭐ 现在一份 SKILL.md 可以驱动多个 agent
□ 但各工具的⭐ 发现目录、支持的扩展字段、加载细节仍可能不同
  → 迁移前查各自文档
□ ⭐ 权威源建议放 .agents/skills/<name>/SKILL.md
```

**一个易混点**：

```
□ 斜杠命令是用户手敲 /xxx 触发
□ ⭐ 技能是 agent 根据任务自动触发
□ 两者机制与用途完全不同，别混为一谈
```

---

## 自查

```
□ 是否用了"三选一"判据（每轮为真→CLAUDE.md / 当做X时→Skill / 绝不→Hook）？
□ CLAUDE.md 是否在 200 行内？
□ ⭐ 是否知道"注意力稀释"——20 条规则每条只分到一小片合规预算？
□ 是否知道压缩后存活的是摘要而非原话？
□ 迁移时是否在 CLAUDE.md 留了一行引用（而非内联）？
□ ⭐ 是否知道"每个会话都适用的规则"不该移进技能？
□ 是否分了用户级/项目级两层？
□ ⭐ 项目专属规则是否下沉到了项目级（避免跨项目瞎套用）？
□ AGENTS.md 与 CLAUDE.md 是否避免了内容重复（防漂移）？
□ 是否用 @导入 或软链，且知道 Windows 软链的限制？
□ ⭐ 是否区分了斜杠命令与自动触发的技能？
□ 是否意识到 hook 是唯一零 token + 确定性的位置？
□ 严禁事项是否用了"禁令 + 指向替代技能"的写法？
□ 跨工具时是否确认了目标工具的发现目录与字段支持？
```
