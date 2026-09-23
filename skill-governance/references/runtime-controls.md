# 可见性与调用控制

## 目录

- [四个可见性状态](#四个可见性状态)
- [两个 frontmatter 开关](#两个-frontmatter-开关)
- [找出没人用的技能](#找出没人用的技能)
- [动态内容注入](#动态内容注入)
- [别名陷阱](#别名陷阱)
- [全局还是项目级](#全局还是项目级)
- [四种机制的分工](#四种机制的分工)

---

## 四个可见性状态

`skillOverrides` 从 settings 控制可见性——**不用改 SKILL.md**。
适合已提交进共享仓库、你不方便编辑的技能。

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

| 值 | 对 Claude 列出 | 在 `/` 菜单 |
|---|---|---|
| `"on"` | 名称 + 描述 | 是 |
| `"name-only"` | 仅名称 | 是 |
| `"user-invocable-only"` | **隐藏** | 是（菜单标为 `user-only`） |
| `"off"` | **隐藏** | **隐藏** |

> **不在 `skillOverrides` 里的技能视为 `"on"`。**
>
> 自 v2.1.199 起，`"off"` 还会把它从 Remote Control 客户端和
> Agent SDK 调用者的命令列表里隐藏。

**⚠️ 按全名调用被隐藏的技能，仍然返回 `skillOverrides` 错误，不会执行。**

**菜单操作**：`/skills` → 高亮技能 → 按 **Space** 循环状态 → **Esc** 保存到
`.claude/settings.local.json`

> **测试神器**：基线对比时用它开关技能，
> **完全不用碰 SKILL.md**（见 `skill-evaluating` 的 `testing.md`）。

---

## 两个 frontmatter 开关

| 字段 | 效果 | 用在哪 |
|---|---|---|
| `disable-model-invocation: true` | **Claude 永不自动触发**，只能手动调用 | 部署、迁移等高风险流程——**只在你明确要求时跑** |
| `user-invocable: false` | 从 `/` 菜单隐藏 | 纯知识型技能，不需要人手动调 |

```yaml
---
name: schema-migration
description: 创建数据库 schema 迁移。
disable-model-invocation: true   # 不希望 agent 自动触发数据库迁移
---
```

> **判断准则**：这个流程"只应在我要求时跑"吗？
> 是 → `disable-model-invocation: true`。

---

## 找出没人用的技能

> ⭐ **列表里的每一个技能，每一轮都在消耗你的上下文——
> 不管 Claude 有没有真的用过它。**

```
/skill-doctor
```

报告内容：
- 每个技能的成本与调用频率
- **标记从未被调用过的技能**，并告诉你去哪关掉
- 也列出最近没用过的插件

> **从成本最高的那批开始关。**

**限制**：
- 需要 v2.1.252+
- 非交互模式加 `-p` 时以文本打印
- 交互模式下在 `/plugin` 管理器的 **Stats** 标签打开
- **Remote Control（手机/浏览器）连接上不可用**——要在跑会话的那台机器的终端执行

---

## 动态内容注入

> `!`command`` 是**动态上下文注入**：Claude Code 先跑命令，
> **把这一行替换成命令输出**，模型才看到技能。
> 也就是说——**指令到达时，你的真实 diff 已经内联在里面了**。

```yaml
---
name: review-changes
---
Review these changes:
!`git diff --staged`
```

**三类动态内容**：

| 类型 | 语法 | 用途 |
|---|---|---|
| **参数** | `$1` / `$ARGUMENTS` | 插值用户输入 |
| **文件包含** | `@style-guide.md` | 引入文件内容 |
| **命令输出** | `` !`cmd` `` | 执行 shell 并嵌入输出 |

> ⚠️ **输出要小**——大 diff 会挤爆上下文。
> 见 `skill-refining` 的 `context-budget.md` 的 Observation Masking。

---

## 别名陷阱

部分内置技能有别名（如 `checkup` 是 `/doctor` 的别名）。

| 场景 | 行为 |
|---|---|
| 在 **managed settings** 或 `--settings` 文件里按**别名**设置 | ✅ 应用到别名背后的技能 |
| 在 **user / project / local** settings 里 | ❌ **只匹配技能真名**——给 `review` 设的对 `review` 生效，不会命中 `/code-review` 的 `/review` 别名 |
| 同时按别名和真名（在 managed settings）设置 | **真名那条优先** |
| 通过别名设置 | **只能进一步限制，不能变得更可见** |
| v2.1.260 之前 | 任何配置源都不应用别名条目 |

**插件技能不受 `skillOverrides` 影响**——改用 `/plugin` 管理。

---

## 全局还是项目级

> **默认放项目级，不要什么都往全局目录堆。**
> 每个全局技能都会出现在每一个会话里——**这会累加**。

**判断准则**（和 npm 一样）：

| 类比 | 位置 |
|---|---|
| `lodash` | 项目里（项目相关） |
| `npm` 本身 | 全局（与具体项目无关） |

> **一个技能配得上全局目录的条件**：
> 它的用处取决于**你怎么工作**，而不是**项目是关于什么的**——
> 尤其是它是那个"用来安装其他技能"的技能（必须在项目存在之前就有）。

> ⚠️ **加载的技能越多 ≠ agent 越聪明。过了某个点，它会变得更糟。**
> （见 `skill-evaluating` 的 `failure-modes.md`：候选池 5 → 100，精确率 29.6% → 3.3%）

**两条经验**：

```
□ 保持库小而聚焦：两三个你真的会用的，胜过二十个你忘了存在的
□ 最小的、能干完活的足迹，通常就是对的那个
```

**冲突时**：个人技能与团队技能触发条件冲突 → **该项目内团队技能优先**。

---

## 四种机制的分工

> **知识 · 触发 · 管道 · 打包**

| 机制 | 是什么 | 关键区别 |
|---|---|---|
| **Skill** | **知识**。教 agent 怎么干一件事，markdown，按 description 按需加载 | 自动触发 |
| **Slash Command** | **手动触发**。你说"现在干这个"，而不是等 agent 决定 | 你调用 |
| **Hook** | **确定性管道**。事件触发跑 shell 命令，**每次都跑，不带判断** | 永远执行，不用于"教" |
| **Plugin** | **打包**。把技能/命令/hooks/MCP 捆在一起一键装 | ⚠️ **仅 Claude Code 专有**，不在开放标准里 |

> **重要提醒**：plugin 的**包装不迁移**到 Cursor 或 Codex
> ——只有它里面的技能可以。

**判断口诀**：

```
要教它怎么干           → Skill
要我手动喊它干         → Command
要"每次 Y 发生就做 X"  → Hook
要打包分发             → Plugin
```

---

## 自查

```
□ 高风险流程是否设了 disable-model-invocation: true？
□ 是否用 skillOverrides 做过基线对比（而非改 SKILL.md）？
□ 是否跑过 /skill-doctor 清理从不调用的技能？
□ 动态注入的命令输出是否够小？
□ 全局目录里的技能是否都通过了"与项目无关"这一关？
□ 是否误用了 hook 去"教"东西（该用 skill）？
□ 是否误用了 skill 去强制某事（该用 hook）？
```
