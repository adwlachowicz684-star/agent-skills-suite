# 技能与子代理的配合

## 目录

- [两种配合模式](#两种配合模式)
- [子代理不继承技能](#子代理不继承技能)
- [三种编排形态](#三种编排形态)
- [Orchestrator 模式](#orchestrator-模式)
- [反模式](#反模式)
- [模型选择策略](#模型选择策略)
- [动态内容](#动态内容)

---

## 两种配合模式

### 模式 1：子代理使用技能（Subagent Uses Skill）

在子代理定义里用 `skills:` 字段列出所需技能。

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and convention compliance
tools: Bash, Glob, Grep, Read
model: inherit
skills: reviewing-cli-command, security-audit
---

Additional instructions for the subagent
```

**执行时**：每个列出的 SKILL.md 的**完整内容**被注入子代理上下文。

### 模式 2：技能在子代理里跑（Skill Runs in Subagent）

在技能的 frontmatter 里设 `context: fork`。

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
```

**执行时**：指定的子代理（或内置 Explore）把技能内容当作任务，在隔离环境中执行，
**只把结果返回给主代理**。

| | 模式 1 | 模式 2 |
|---|---|---|
| 声明位置 | 子代理的 `skills:` | 技能的 `context: fork` |
| 谁控制 | 子代理作者 | 技能作者 |
| 上下文 | 子代理启动时注入全文 | 隔离执行，只回传结果 |

---

## 子代理不继承技能

> ⚠️ **与主代理不同，子代理不从父对话继承技能。技能必须在其 `skills:` 字段里显式声明。**

这是一个高频故障点：主代理能用某个技能，派出去的子代理却"不知道"它。

**另一个差异**：主代理走**渐进式披露**（按需加载），
而子代理是**启动时全文注入**——所以给子代理挂技能要**克制**，别一次挂五个。

---

## 三种编排形态

| 形态 | 适用 | 结构 |
|---|---|---|
| **单技能消费者** | 聚焦的单一领域任务 | 1 个技能 + 最小工具集 |
| **多技能编排者** | 跨领域工作流 | 2+ 技能 + Task 工具 |
| **增强型** | 需要代码库理解 + 会话连续性 | 加 Skill 工具做动态发现 |

**单技能消费者**：

```yaml
name: sql-agent
skills: sql-helper
tools: ["Read", "Grep", "Glob"]
```
✅ 快、聚焦、职责清晰 ❌ 只限一个领域

**多技能编排者**：

```yaml
name: fullstack-orchestrator
skills: frontend-design, api-generator, migration-patterns
tools: ["Read", "Write", "Bash", "Task"]
```
✅ 处理复杂工作流 ❌ 决策开销更大

> 多技能时要写清"什么时候用哪个技能"，并注明"**简单请求不要激活全部技能**"。

---

## Orchestrator 模式

> **外层技能变成编排者**——它调用各个子代理，收集结果，决定下一步。

```yaml
---
name: research-changes
description: Research recent code changes and their impact
subagent: true
---
分析本仓库最近的变更……

---
name: validate-tests
description: Run tests and validate coverage for recent changes
subagent: true
---
验证测试套件……

---
name: health-check
description: Full project health check
---
1. 先用 /research-changes 了解最近变更
2. 再用 /validate-tests 验证测试套件
3. 最后综合两边的发现
```

**执行**：调用 `/health-check` → 在主代理跑编排者 → 调 `/research-changes`（**派生子代理**）→
再调 `/validate-tests`（**再派生子代理**）→ 编排者综合结果。

> **好消息**：一个子代理技能在调用其他技能时，**不会再派生子代理**，即使那些技能标了
> `subagent: true`——它们改为内联执行。
> → **不用担心无限嵌套，编排模式总是一层深。**

---

## 反模式

### ❌ 循环依赖

```
subagent-a → subagent-b → subagent-a   // 无限循环
```

✅ 正确：

```
orchestrator → specialist-a
orchestrator → specialist-b
（专家之间不互相调用）
```

### ❌ 技能过载

```markdown
1. Invoke skill-1  2. Invoke skill-2  3. Invoke skill-3
4. Invoke skill-4  5. Invoke skill-5
```

加载太多技能浪费上下文。

✅ 正确：

```markdown
1. 分析代码语言
2. 只调用相关的那个 style guide 技能
3. 应用指南
```

### ❌ 用 Read 直接读技能文件

有 Skill 工具的 agent **必须**用 `Skill("plugin:skill-name")` 加载，
而不是 `Read` 技能文件或 `Grep` 找模式。

---

## 模型选择策略

| 角色 | 模型 | 理由 |
|---|---|---|
| 主代理（编排、复杂推理） | 强模型 | 需要推理能力 |
| 子代理（专门、窄任务） | **便宜模型** | 任务窄，不需要强推理 |

**实测**：三个研究子代理改用 haiku，总成本从 **$6.35 降到 $3.43**，任务完成效果维持。

> 这是最省钱的单一杠杆：**编排用强模型，执行用便宜模型。**

---

## 动态内容

技能正文支持三类动态内容：

| 类型 | 语法 | 用途 |
|---|---|---|
| **参数** | `$1`、`$ARGUMENTS` | 插值用户输入 |
| **文件包含** | `@style-guide.md` | 引入文件内容（相对配置目录） |
| **命令输出** | `` !`git diff --staged` `` | 执行 shell 并嵌入输出 |

```yaml
---
name: review-changes
---
Review these changes:
!`git diff --staged`
```

> 命令输出注入很强大（模型看到的是真实 diff，不是命令本身），
> 但注意**输出要小**——大 diff 会挤爆上下文。

---

## 权限

技能可以定义自己的权限作用域：

```yaml
permissions:
  allow:
    - Read(src/**)
    - Exec(npm run test)
  deny:
    - Write(/etc/**)
  ask:
    - Write(src/**)
```

> **技能权限是叠加的，不是替换**——它不能授予在上层（项目/组织）被拒绝的权限。

`allowed-tools` 未指定时技能**拥有全部工具**。
**安全关键的技能一定要限制到最小集。**

---

## 自查

```
□ 子代理是否显式声明了它需要的技能？（它不继承！）
□ 给子代理挂的技能是否过多？（启动时全文注入）
□ 是否存在子代理互相调用的循环？
□ 编排是否只有一层深？
□ 执行型子代理是否用了更便宜的模型？
□ 安全关键技能是否限制了 allowed-tools？
□ 用 Skill 工具而非 Read 来加载技能？
```
