# frontmatter 全字段：四组与开放标准边界

> 相关：《skill-structuring》的 `frontmatter-pitfalls.md` ·
> `invocation-control-fields.md` · 《skill-crafting》的
> `argument-substitution.md`
> 前置：那些讲"常见错误"和"调用控制"，
> 这份做⭐ **完整字段字典 + 可移植性边界**。

---

## 目录

- [1. ⭐⭐ 开放标准 vs Claude Code 扩展](#1--开放标准-vs-claude-code-扩展)
- [2. 身份与触发组](#2-身份与触发组)
- [3. 调用与参数组](#3-调用与参数组)
- [4. 执行环境组](#4-执行环境组)
- [5. ⭐ 高级执行组](#5--高级执行组)
- [6. ⭐ 调用控制三档对照](#6--调用控制三档对照)

---

## 1. ⭐⭐ 开放标准 vs Claude Code 扩展

> ⭐ **开放标准只定义 6 个字段**：
> `name` · `description` · `license` · `compatibility` · `metadata` · `allowed-tools`
> ⭐ **其余全部是 Claude Code 扩展**。

**这个边界决定了可移植性**：

```
⭐ 只用通用三件套
   → 在 Claude Code / Codex / Cursor / Copilot 等 40+ 工具间
     ⭐ 直接复制就能用

⭐ 用了 CC 扩展字段（context: fork、hooks 等）
   → 到其他工具里⭐ 这些字段被忽略或报警
   → ⭐ 核心指令仍可用，但⭐ 行为可能退化
```

**其他实现者的取舍**：

```
Cursor   也实现了 paths 和 disable-model-invocation（语义相同）
Codex    ⭐ 对应能力放在边车文件 agents/openai.yaml 里，
         ⭐ 而不是 frontmatter
```

---

## 2. 身份与触发组

**`name`**

```
小写字母 + 数字 + 连字符，1–64 字符
⭐ 开放标准额外要求：
   不得以连字符开头/结尾
   不得含连续连字符 --
   ⭐ 必须与父目录名一致
⭐ Anthropic 平台保留词：name 里不可含 anthropic / claude
（Claude Code 中可省略，省略时取目录名）
```

**`description`**

```
⭐ 回答两个问题：做什么 + 何时用，并埋入你实际会说的触发词
≤1024 字符
⭐ SEO 另有一条：150–160 字符是甜点区（对注册表展示而言）
```

**多行写法**（YAML 块标量）：

```yaml
description: |
  Multi-line description block.
  ⭐ 需要 2–3 句又不想转义引号时用这个，保持 YAML 可读
```

**`when_to_use`**

```
⭐ 触发场景的补充区
⭐ 与 description 合并计入 ⭐ 1536 字符预算，一起参与匹配
⭐ 适合放长尾触发词、中英文别名
```

**`paths`** ⭐（很多教程没提，但很实用）

```yaml
paths:
  - src/api/**
  - server/routes/**
```

> ⭐ **用 glob 把技能的"自动可用性"限定在特定文件范围**
> ——只有对话涉及匹配路径的文件时，这个技能才进入候选。
>
> ⭐ **monorepo 利器，也能避免无关任务误触发。**

> ⭐ 这直接回应了 `skillsbench-vs-realworld.md` 的核心问题：
> **减少候选 = 提高加载率 16%→更高**。

---

## 3. 调用与参数组

```yaml
argument-hint: "[issue-number] [priority]"   # 纯展示
arguments: issue priority                     # 声明命名参数
disable-model-invocation: true                # 禁止自动触发
user-invocable: true                          # 是否在 / 菜单显示
```

**参数替换体系**（正文中可用）：

| 占位符 | 含义 |
|---|---|
| `$ARGUMENTS` | 全部参数原文 |
| `$ARGUMENTS[0]` / `$ARGUMENTS[1]` | 第 N 个参数（0 起） |
| `$0` / `$1` | 上面两个的简写 |
| `$名字` | `arguments` 声明的命名参数 |

```
⭐ 正文里没写 $ARGUMENTS 时，参数自动追加到内容末尾
⭐ 参数按 shell 风格切分：/skill "multi word" arg
   → $0 = multi word，$1 = arg
```

> ⚠️ 与 `argument-substitution.md` 的关键提醒配套：
> **替换在加载时执行**，所以正文里任何长得像 `$1` 的代码（bash 函数、
> awk）都会被替换——**含 `$N` 的代码示例必须移进 reference 文件**。

**`disable-model-invocation: true` 的三重效果**（很值）：

```
① Claude 不能自动触发，只能手动 /name
② ⭐ 该技能的 description 不进入启动时的元数据列表 → ⭐ 省 token
③ 不可被 subagent 预加载
```

> ⭐ **这就是"传统斜杠命令"的现代写法**——
> 适合有副作用、不想被误触发的操作（部署、群发、清理）。

---

## 4. 执行环境组

```yaml
allowed-tools: Read, Grep, Glob, Bash(git log *)
disallowed-tools: [...]      # ⭐ 激活期间从工具池⭐ 移除指定工具
model: haiku                 # 别名 / 完整 ID / inherit
effort: low                  # low–max
shell: bash                  # !`命令` 动态注入用哪个 shell
```

**`model`** 的取值与用途：

```
别名（opus / sonnet / haiku）⭐ 比完整 ID 更耐久（跨模型发布）
   需要强推理   → opus
   简单文本快转 → haiku
   ⭐ 成本敏感的批处理 → haiku
```

**`disallowed-tools`** 常被忽略但很有用：

```
⭐ 与 allowed-tools 是两种思路：
   allowed-tools    = 白名单（只许用这些）
   disallowed-tools = ⭐ 黑名单（从现有工具池里移除这些）
   → 想"保留大部分能力、只禁掉少数"时用后者
```

**一个重要的安全提示**：

```
⭐ 声明 allowed-tools 或 hooks 的技能，
   ⭐ 首次使用需要用户批准——运行时把它们当作"提权请求"。
```

**环境变量**（引用自带脚本时的标准写法）：

```
${CLAUDE_SESSION_ID}   当前会话 ID
${CLAUDE_EFFORT}       当前 effort
⭐ ${CLAUDE_SKILL_DIR}   ⭐ 技能自身所在目录的绝对路径
   ——⭐ 引用自带脚本时的标准写法：!`python ${CLAUDE_SKILL_DIR}/x.py`
```

> ⭐ `${CLAUDE_SKILL_DIR}` 这条解决了"技能被装到不同位置后
> 脚本路径失效"的老问题——**永远用这个变量而不是相对路径**。

---

## 5. 速查

```
⭐ 开放标准只 6 个字段，其余是 CC 扩展
□ 只用通用字段 → 40+ 工具可复制
□ 用 CC 扩展 → 别处被忽略，核心可用但行为退化
□ Cursor 支持 paths / disable-model-invocation
□ Codex 放在 agents/openai.yaml（不在 frontmatter）

身份触发：
□ name：1–64 字符，⭐ 不得 -- 连续、⭐ 须与目录名一致
□ ⭐ name 不可含 anthropic / claude
□ description：做什么 + 何时用 + 触发词，≤1024（⭐ SEO 150–160）
□ when_to_use：⭐ 与 description 合并计 1536
□ ⭐ paths：glob 限定自动可用性（monorepo 利器）

调用参数：
□ argument-hint（展示）/ arguments（命名参数）
□ $ARGUMENTS / $0 / $名字
□ ⭐ disable-model-invocation：禁自动 + ⭐ 省元数据 token + 不可被预加载
□ ⚠️ 含 $N 的代码示例必须移进 reference（加载时会被替换）

执行环境：
□ allowed-tools（白名单）/ ⭐ disallowed-tools（黑名单）
□ ⭐ 声明 allowed-tools 或 hooks → 首次使用需用户批准
□ model 用别名更耐久；effort；shell
□ ⭐ ${CLAUDE_SKILL_DIR} 引用自带脚本（不要相对路径）

高级字段（context: fork / agent / hooks / 调用控制三档）
→ 见 `frontmatter-advanced-fields.md`
```

**一句话**：

> ⭐ **`paths` 用 glob 把技能的"自动可用性"限定在特定文件范围——
> 这是唯一能直接减少候选集、从而提高加载率的字段。**
