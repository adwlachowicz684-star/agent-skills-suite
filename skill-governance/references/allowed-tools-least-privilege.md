# 最小权限：allowed-tools 的四面红旗

> 相关：《skill-governance》的 `skill-invocation-control.md` ·
> `security-audit-ops.md` · 《skill-structuring》的 `invocation-control-fields.md`
> 前置：`skill-invocation-control.md` 讲权限规则语法，
> 这份讲⭐ **如何从声明判断一个技能是否过度授权**。

---

## 目录

- [1. ⭐⭐ 前提：权限必须由运行时强制](#1--前提权限必须由运行时强制)
- [2. ⭐⭐ 四面红旗](#2--四面红旗)
- [3. 作者侧四条最佳实践](#3-作者侧四条最佳实践)
- [4. 使用者侧四条](#4-使用者侧四条)
- [5. ⭐ 平台差异与"没有绝对安全的工具"](#5--平台差异与没有绝对安全的工具)

---

## 1. ⭐⭐ 前提：权限必须由运行时强制

> ⭐⭐ **权限必须由宿主运行时强制，而不是靠给模型的提示指令。**
> **在处理对抗性提示时，不能信任 LLM 会自我执行访问限制。**

> ⭐ 这一条是所有后续讨论的地基。
> 它与 `determinism-boundary.md` 的
> "把破坏性拦截写进技能是表演"完全同源：
> **声明只是意图，执行侧的强制才算数。**

三层防御纵深：

```
第 1 层  声明与摄入：Unicode/密钥清洗 → 静态 AST+正则审计 → LLM 语义策略审计
第 2 层  权限强制：allowed-tools 边界门 → 文件系统路径 jail / 沙箱
第 3 层  运行时隔离：WASM / MicroPython worker，或 MicroVM / Docker + eBPF
```

---

## 2. ⭐⭐ 四面红旗

**🚩 红旗 1：工具太多**

```
bash · curl · wget · python · node · docker · ssh · sudo
```

> ⭐ **没有任何正当技能需要全部这些。**
> 这要么是设计糟糕（过度授权），要么是恶意（最大化攻击面）。

**🚩 红旗 2：危险组合**

```
bash + curl
```

> ⭐ 既能执行命令，又能外传数据。
> 这是**数据窃取、反向 shell、恶意投递**的经典组合。

**🚩 红旗 3：工具与描述不匹配**

```
描述："检查 git 提交信息的技能"
工具：bash · curl · nmap · metasploit
```

> ⭐ 一个 git 技能为什么需要网络扫描和渗透测试工具？
> **声明与用途不符是最强的恶意信号。**

**🚩 红旗 4：动态执行**

```
bash · eval · exec
```

> ⭐ 可以执行作为参数传入的任意代码。**极度危险。**

---

## 3. 作者侧四条最佳实践

**① 最小权限**

```
❌ bash · curl · python · node · docker
✅ git · grep
```

**② ⭐ 说明为什么需要**

```
## Tools
- psql

## Why
本技能查询 PostgreSQL 生成报表。
⭐ 只跑 SELECT，不修改数据。
```

> ⭐ 这与 `write-reasons-not-rules.md` 同源：写原因。
> 而且在安全场景，写原因是**可审计性**的要求。

**③ 能用只读就用只读**

```json
{"allowed-tools": ["git", "grep", "cat"], "permissions": {"read_only": true}}
```

**④ ⭐ 避免 shell 执行**

```
❌ tools: bash
   commands: bash -c "git log --oneline"

✅ tools: git
   commands: git log --oneline
```

> ⭐ 这条最值得抄：**能用具体工具就别用 bash**。
> `Bash(python:scripts/*)` 也比裸 `Bash` 好得多。

**粒度递进**（从宽到严）：

```
Read                     只读文件系统
Write                    写（通常要限定目录）
Bash                     任意 shell（最高权限，慎用）
Bash(python:*)           只允许执行 python
⭐ Bash(python:scripts/*) 只允许执行 scripts/ 下的 python
WebFetch / WebSearch     网络
```

---

## 4. 使用者侧四条

```
① ⭐ 安装前务必检查 allowed-tools
   看到 bash + curl / sudo / eval → 停下来审计完整代码
② 优先选 read_only: true 或工具集最小的
③ ⭐ 在隔离环境先试（mkdir ~/skill-test，装进去跑一遍）
④ 用扫描器自动标记过度授权的技能
```

---

## 5. ⭐ 平台差异与"没有绝对安全的工具"

**平台差异**（同一件事三种写法）：

```
Claude Code    allowed-tools 数组 + permissions 对象（可设 read_only）
GitHub Copilot skills[].tools（YAML 数组，⭐ 粒度较粗）
OpenAI Codex   tools + sandbox（可设 network:false / filesystem:read_only）
```

**一个值得记住的 Q&A**：

```
Q: 只有 "git" 的技能仍然危险吗？
A: ⭐ 是的，只是程度低一些。
   它可以克隆恶意仓库、通过提交到外部仓库外传数据、修改 git hooks。
   ⭐ 但它不能直接执行任意代码或访问 git 仓库之外的文件。
```

> ⭐ 这个回答的分寸感很好：**最小权限不是零风险，是降低风险上限。**

**相对低风险的工具**（供参考，非绝对）：

```
git（读历史）· grep · ls · cat（但要确认读的是哪些文件）
```

**两个常见问题的答案**：

```
Q: 能不能装完之后再限制工具的权限？
A: ⭐ 一般不能。技能自己定义所需工具。
   能做的是：fork 后改 SKILL.md、用沙箱限制运行时、换一个权限更小的技能。

Q: "tools" 和 "allowed-tools" 有什么区别？
A: 是同一个东西，只是不同平台的命名不同。
```

---

## 速查

```
前提：
□ ⭐⭐ 权限必须由运行时强制（不能靠提示指令让模型自我限制）
□ 三层纵深：声明摄入 / 权限强制 / 运行时隔离

⭐ 四面红旗：
□ 🚩 工具太多（bash+curl+wget+python+node+docker+ssh+sudo）
□ 🚩 危险组合（bash + curl = 能执行 + 能外传）
□ 🚩 工具与描述不匹配（git 技能要 nmap）
□ 🚩 动态执行（bash/eval/exec）

作者侧：
□ ⭐ 最小权限
□ ⭐ 写清"为什么需要这个工具"
□ ⭐ 能只读就只读
□ ⭐⭐ 能用具体工具就别用 bash（git 而非 bash -c "git log"）
□ 粒度：Bash(python:scripts/*) > Bash(python:*) > Bash

使用者侧：
□ ⭐ 装前检查 allowed-tools
□ 优先 read_only
□ 隔离环境先试
□ 用扫描器
□ ⭐ 最小权限 ≠ 零风险，是降低上限
```

**一句话**：

> ⭐⭐ **"bash + curl"意味着既能执行命令又能外传数据——
> 这是数据窃取和反向 shell 的经典组合。**
