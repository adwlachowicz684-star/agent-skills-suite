# allowed-tools 完整参考：工具表与 Bash 作用域

> 相关：《skill-governance》的 `allowed-tools-least-privilege.md`（四面红旗）·
> `pre-install-security-audit.md` · 《skill-structuring》的
> `frontmatter-fields.md` · `official-spec-and-style.md`
> 前置：那份讲"最小权限的原则与危险组合"，
> 这份是⭐⭐ **可查的完整清单**：有哪些工具名、Bash 怎么收窄、常见组合怎么配。

---

## 目录

- [1. ⭐⭐ 它是怎么强制的](#1--它是怎么强制的)
- [2. ⭐⭐ 完整工具表](#2--完整工具表)
- [3. ⭐⭐⭐ Bash 作用域语法](#3--bash-作用域语法)
- [4. ⭐ 按技能类型推荐组合](#4--按技能类型推荐组合)
- [5. ⭐⭐ 格式细节与易错点](#5--格式细节与易错点)

---

## 1. ⭐⭐ 它是怎么强制的

> ⭐⭐ **`allowed-tools` 控制技能在运行时可以调用哪些工具。**
> ⭐⭐⭐ **Claude Code ⭐ 严格执行这个列表——
> 技能试图调用不在列表里的工具，⭐ 调用被阻止。**

这与我们此前反复强调的那条要区分开：

```
⭐ 声明在技能里 = 意图（说明）
⭐⭐⭐ 执行侧强制 = ⭐ 这个字段（以及权限规则、MCP server 参数、沙箱）
```

> ⭐⭐ 所以 `allowed-tools` 是少数⭐ **真正在执行侧生效的技能内声明**。
> 但它仍然是"允许"而不是"拒绝"——
> ⭐ 它不能扩大用户已授予的权限，只能⭐ 收窄到这个技能需要的子集。
> 这与 `determinism-boundary.md` 的
> "Hooks 用于模型不可被信任去遵守的事"是同一层的不同机制。

---

## 2. ⭐⭐ 完整工具表

**文件系统**

| 工具 | 作用 | 什么时候用 |
|---|---|---|
| `Read` | 读文件（含图片、PDF、Jupyter） | ⭐ 需要检查现有文件、分析代码 |
| `Write` | 创建或⭐ 完整覆盖 | 生成新文件、整体重写 |
| `Edit` | ⭐ 精确字符串替换 | ⭐ **部分更新优先于 Write** |
| `Glob` | 按模式找文件路径 | 先发现文件再处理 |
| `Grep` | 正则搜内容（基于 ripgrep） | 找模式、函数定义、import |

**执行 / 网络**

| 工具 | 作用 |
|---|---|
| `Bash` | 执行 shell 命令（见下节作用域） |
| `WebFetch` | 抓 URL 内容 |
| `WebSearch` | 联网搜索 |

**Agent 与任务**

| 工具 | 作用 | 什么时候用 |
|---|---|---|
| `Task` | 创建并管理子代理任务 | 委派复杂子任务或并行 |
| ⭐ `Skill` | ⭐ **按名字调用另一个技能** | ⭐ 编排/链式依赖另一个技能的输出 |
| `AskUserQuestion` | ⭐ 执行中向用户提问（会暂停等待） | 需要无法从上下文推断的决策 |

**工作区**

| 工具 | 作用 |
|---|---|
| `TodoWrite` | 待办与清单 |
| `NotebookEdit` | 编辑 .ipynb 单元格 |

> ⭐⭐ `Skill` 这个工具值得单独注意：
> ⭐⭐⭐ **技能组合（依赖注入/链式）需要显式声明 `Skill` 才能调用别的技能。**
> 这与 `skill-dependency-injection.md` 的四种模式直接相关——
> ⭐ **正文里写了 `/pdf`，但 `allowed-tools` 里没有 `Skill`，调用会被阻止。**
> 这是一条很容易漏的对应关系。

> ⭐ `AskUserQuestion` 也要小心：
> 它与 `preflight-gate.md` 的"不得中途暂停去要一个 STEP 0 本可收集到的输入"
> 存在张力——⭐ **前置门禁阶段该用 AskUserQuestion 一次问完，
> 而不是执行中途反复问**。

---

## 3. ⭐⭐⭐ Bash 作用域语法

```
语法：Bash(prefix:*)
⭐ * 通配前缀之后的任意字符
```

**常用模式**：

| 模式 | 允许 | 例子 |
|---|---|---|
| `Bash(npm:*)` | npm | npm install / run build / test |
| `Bash(git:*)` | git | status / diff / log |
| `Bash(docker:*)` | docker | build / run / ps |
| `Bash(kubectl:*)` | kubectl | get pods / describe / apply |
| `Bash(terraform:*)` | terraform | plan / apply / validate |
| `Bash(python3:*)` | python | script.py / -m pytest |
| `Bash(cargo:*)` | cargo | build / test / clippy |
| `Bash(pnpm:*)` | pnpm | install / build |

**可以多个并存**：

```yaml
allowed-tools: Read, Write, Bash(npm:*), Bash(git:*), Bash(docker:*)
```

**不加作用域 = 完全放开**：

```yaml
allowed-tools: Read, Bash     # ⭐ 任意 shell 命令
```

> ⭐⭐ 官方的说法很克制但准确：
> **"只在技能确实需要广泛命令访问时才用无作用域 Bash——
> 比如一个可能需要跑任意诊断命令的调试技能。"**
>
> ⭐⭐⭐ 这与 `allowed-tools-least-privilege.md` 那条
> "能用具体工具就别用 bash（用 `git` 而不是 `bash -c "git log"`）"
> 完全一致，只是这里给出了⭐ 折中档：
> **不需要完全放开时，`Bash(git:*)` 比裸 `Bash` 好得多。**

---

## 4. ⭐ 按技能类型推荐组合

```
只读分析类：
  Read, Glob, Grep
  （⭐ 官方明确列出：适合只读技能、安全敏感工作流、限定范围操作）

生成文件类：
  Read, Write, Edit, Glob

需要跑命令类：
  Read, Grep, Bash(<具体前缀>:*)
  ⭐⭐ 不要裸 Bash

编排类（要调用别的技能）：
  ⭐ Skill, Read, TodoWrite
  ⭐⭐ 忘了 Skill 就会调用被阻止

调试类：
  ⭐ Bash（无作用域，唯一合理的例外场景）+ Read + Grep
```

---

## 5. ⭐⭐ 格式细节与易错点

```
· ⭐ accepted 形式：⭐ 逗号分隔的字符串（也有说空格分隔/ YAML 列表）
  ⭐⭐⭐ 各实现不一致——以你目标平台为准（呼应"实验性，各实现支持不一"）
· ⭐⭐ 工具名⭐ 大小写敏感，必须完全匹配
· ⭐ 配错时不是"忽略该字段"，而是⭐⭐ 调用不在列表里的工具被阻止
```

> ⭐⭐⭐ 最后一条的实践含义：
> **配得不够会导致技能跑到一半被拦下来**——
> 症状很像"技能没写完"，实际是权限不够。
> ⭐ **排查"技能中途失败"时，先看是不是它想用一个没声明的工具。**

**一个与其他来源的出入**（如实标注）：

```
本来源：allowed-tools 是"逗号分隔的字符串"
另一来源（open standard）：⭐ 空格分隔的列表
⭐ 仲裁：⭐⭐ 两者都见于真实文档，说明⭐ 实现差异确实存在。
   稳妥做法：优先用你目标平台上⭐ 已验证可用的写法，
   并在跨平台分发时⭐ 实际测一次（呼应 cross-agent-portability.md）。
```

---

## 速查

```
□ ⭐⭐⭐ ⭐ 严格执行：不在列表里的工具，调用被阻止
   ⭐ 它是"允许"不是"拒绝"——只能收窄，不能扩大已有权限

□ ⭐⭐ 工具：Read/Write/Edit(⭐部分更新优先)/Glob/Grep
        Bash/WebFetch/WebSearch
        Task/⭐ Skill(⭐ 调别的技能必声明)/AskUserQuestion
        TodoWrite/NotebookEdit
□ ⭐⭐⭐ ⭐ 正文写了 /pdf 但 allowed-tools 没有 Skill → 被阻止

□ ⭐⭐⭐ Bash(prefix:*)：npm/git/docker/kubectl/terraform/python3/cargo/pnpm
   ⭐ 可多个并存
   ⭐⭐ 裸 Bash = 任意命令，⭐ 只在该技能确实需要时（调试类）
□ ⭐ 只读类：Read, Glob, Grep

□ ⭐⭐ 大小写敏感 · ⭐ 格式（逗号/空格/YAML列表）各实现不一，⭐ 实测为準
□ ⭐⭐⭐ ⭐ 配得不够 = 技能跑到一半被拦（症状像"没写完"）
```

**一句话**：

> ⭐⭐⭐ **allowed-tools 是少数真正在执行侧生效的技能内声明——
> 不在列表里的工具调用会被直接阻止；
> 所以编排类技能忘了写 `Skill` 就会调不动别的技能，
> 而"技能跑到一半失败"很可能不是没写完，是权限没给够。**
