# frontmatter 高级字段：fork、agent、hooks 与调用控制

> 相关：《skill-evaluating》的 `frontmatter-full-reference.md`（基础四组）·
> 《skill-structuring》的 `invocation-control-fields.md` ·
> `frontmatter-pitfalls.md` · 《skill-orchestration》的
> `context-isolation-fork.md`
> 前置：基础字段见 `frontmatter-full-reference.md`。
> 这份只讲⭐ **高级执行组与调用控制的三种组合**。

---

## 目录

- [1. ⭐ 高级执行组](#1--高级执行组)
- [2. ⭐ 调用控制三档对照](#2--调用控制三档对照)
- [3. ⚠️ 一处术语冲突](#3--一处术语冲突)

---

## 1. ⭐ 高级执行组

```yaml
context: fork        # 在 fork 出的子代理上下文中执行
agent: Explore       # 配合 context: fork 指定子代理类型
hooks:               # 仅技能激活期间生效的生命周期 hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
```

**内置 agent 三档**（选择依据写得很清楚）：

| agent | 模型 | 工具 | 用途 |
|---|---|---|---|
| Explore | Haiku | 只读 | 快速代码库搜索分析 |
| Plan | 继承 | 只读 | 预规划研究 |
| general-purpose | 继承 | 全部 | 复杂多步任务 |

```
⭐ .claude/agents/ 里的自定义 agent 也可按名字引用
⭐ 用 context: fork 时，Stop hooks 在运行时会转为 SubagentStop 事件
```

> ⚠️ 配套提醒（见 `context-isolation-fork.md`）：
> **fork 的正文如果写得"像一份技能规格"，会被子代理模式匹配成派发请求，
> 递归调用自己**——所以 fork 正文要写成直接的命令式步骤。

---

## 2. ⭐ 调用控制三档对照

| 配置 | 用户可 /name | Claude 可自动 | 在上下文里 |
|---|---|---|---|
| （默认） | ✅ | ✅ | ✅ |
| `disable-model-invocation: true` | ✅ | ❌ | ❌ |
| `user-invocable: false` | ❌ | ✅ | ✅ |

**两个典型用法**（官方给的，很清晰）：

```yaml
# 部署这类有时序要求的副作用流程
name: deploy
disable-model-invocation: true
```

```yaml
# 纯背景知识，用户手动调用没意义
name: api-conventions
user-invocable: false
```

**⚠️ 一处术语冲突（务必注意）**：

```
不同文档对 user-invocable 的⭐ 默认值说法不一致：
  一份说 default false（需显式开启才有 slash 命令）
  一份说 default true（默认可见，设 false 才隐藏）

⭐ 实践建议：不依赖默认值，显式写出这个字段。
```

---

## 3. ⚠️ 一处术语冲突（务必注意）

```
不同文档对 user-invocable 的⭐ 默认值说法不一致：
  一份说 default false（需显式开启才有 slash 命令）
  一份说 default true（默认可见，设 false 才隐藏）

⭐ 实践建议：⭐ 不依赖默认值，显式写出这个字段。
```

> ⭐ 这与 `frontmatter-pitfalls.md` 里"静默失败"一脉相承：
> **凡是文档之间有分歧的字段，都要显式写出来，别赌默认行为。**

---

## 速查

```
高级执行：
□ context: fork 在隔离子代理中执行
□ ⭐ agent 三档：Explore（Haiku/只读/快搜）· Plan（继承/只读/预规划）
                · general-purpose（继承/全工具/复杂多步）
□ .claude/agents/ 里的自定义 agent 可按名字引用
□ hooks 四种类型（command/http/prompt/agent），仅技能激活期生效
□ ⭐ 用 context: fork 时 Stop hooks 会转为 SubagentStop 事件
□ ⚠️ fork 正文别写成"像技能规格"，会被模式匹配成派发请求而递归自调用

调用控制三档：
□ 默认：用户✅ Claude✅
□ disable-model-invocation: true：用户✅ Claude❌（⭐ 省元数据 token）
□ user-invocable: false：用户❌ Claude✅（纯背景知识）
□ ⭐ 有副作用的流程用前者；纯背景知识用后者

□ ⚠️ user-invocable 默认值说法冲突 → ⭐ 显式写出
□ ⭐ 声明 allowed-tools 或 hooks → 首次使用需用户批准（视为提权请求）
```

**一句话**：

> ⭐ **部署这类有副作用的流程用 `disable-model-invocation: true`——
> 它同时买到两样东西：不会被误触发，以及不占元数据 token。**
