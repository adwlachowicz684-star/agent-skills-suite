# 技能不触发：九项排查（按此顺序）

> 相关：《skill-evaluating》的 `troubleshooting-manual.md` ·
> `reload-debug.md` · 《skill-crafting》的 `skill-structuring` 的 `frontmatter-pitfalls.md`

---

## 目录

- [1. ⭐ 为什么必须按顺序](#1--为什么必须按顺序)
- [2. 九项排查](#2-九项排查)
- [3. ⭐ 核心隔离法：显式调用](#3--核心隔离法显式调用)
- [4. ⭐ 两个流传很广的错误说法](#4--两个流传很广的错误说法)
- [5. 五分钟真实排障](#5-五分钟真实排障)

---

## 1. ⭐ 为什么必须按顺序

> ⭐ **发现、YAML 解析、描述匹配全都在内部进行，
> 没有任何面向用户的错误路径。**
>
> ⭐ **"考虑过但拒绝了" 与 "对 Claude 而言根本不存在"
> 两者没有可区分的错误状态——
> 这正是按顺序排查比瞎猜更重要的原因。**

---

## 2. 九项排查

**① 文件名与目录布局**

```
⭐ 必须叫 SKILL.md —— 全大写，一字不差
  不是 skill.md · 不是 Skill.MD · 不是 SKILLS.md

✅ ~/.claude/skills/excel-reports/SKILL.md
❌ ~/.claude/skills/SKILL.md           ← 散落文件，被忽略
```

> ⭐ 每个技能必须是**自己名字的目录**，不能是散落的 md 文件。

**② 目录位置**

```
~/.claude/skills/    个人技能，所有项目可用
.claude/skills/      项目技能，随仓库提交
```

> 把技能放进项目目录、却从别的目录运行 Claude → 找不到。

**③⭐ 重启会话**

```
⭐ 技能在会话开始时扫描。
⭐ 会话中途新增或修改 → Claude 没看到变化。
```

**④⭐ description —— 头号原因**

```
❌ "Helps with spreadsheets"
✅ "Create formatted .xlsx spreadsheets with formulas and charts.
    Use when the user asks for an Excel file, a spreadsheet,
    or a financial model."
```

要点：**第三人称 · 说明做什么 + 何时用 · 含用户真正会输入的词**。

**⑤ frontmatter 合法**

```
⭐ 开闭 --- 都要有 · 键合法 · ⭐ 不能有游离的 tab
⭐ 未加引号的值里避免裸冒号和尖括号
⭐ 描述别超长（会被截断）
```

**⑥ 确认已启用**

```
Claude Desktop：settings/permissions 里确认功能与具体技能已开
Claude Code：   确认不在受限权限模式；
                ⭐ 若期望自动触发，检查是否设了 disable-model-invocation
```

**⑦ 权限 / 临时目录阻塞**

```
脚本跑失败，常是工作目录或临时目录的文件系统权限问题
（例如被锁死的 /tmp）
确认：能读技能目录、能写 scratch 目录、bundled 文件可读（不是 chmod 000）
```

**⑧ 显式调用做隔离**（见下节）

**⑨ 更新客户端 + 查 changelog**

```
⭐ 技能是较新的能力，加载行为随版本变过。
⭐ "昨天还好好的今天坏了，而我什么都没改" → 大概率是规范随更新变了
```

---

## 3. ⭐ 核心隔离法：显式调用

> ⭐ **按名字显式调用（如 `/excel-reports`）来隔离问题：**
>
> ```
> 显式调用成功、自动调用失败
>   → ⭐ 技能装好了，问题在 description（回到第 ④ 步）
> ```

一步就分开了"发现/加载"与"触发"两个故障域。

**确认是否加载**的技巧：

```
/tdd
你刚刚加载了 tdd 技能。确认一下，并用一句话总结它的指令。
```

> ⭐ **加载了 → 能准确描述；没加载 → 回答很笼统。**
> 这与 `reload-debug.md` 的"验证要靠它复述"完全一致。

---

## 4. ⭐ 两个流传很广的错误说法

**误区一："改了技能要重启 Claude Code"**

```
⭐ 错误。实时变更检测会在当前会话内发现新技能。
⭐ 唯一例外：⭐ 如果 .claude/skills/ 这个目录本身
   在会话开始时不存在、是你刚创建的，才需要全新会话。
   已存在目录里的单个技能文件是实时被发现的。
```

**误区二："编号文件夹决定优先级"**

```
⭐ 错误。Claude 不从文件夹名读优先级，
   项目内没有文件夹编号优先级。
⭐ 唯一的覆盖顺序是 enterprise > personal > project
   （越全局越赢，与直觉相反）
⭐ 数字前缀只是让你 ls 的时候整齐。
```

> ⭐ 这两条几乎出现在每一份老的排障指南里，**都是错的**。

---

## 5. 五分钟真实排障

```
症状：Claude 写了 Jest 断言，但测试技能指定的是 Vitest

① 问它"这里该用什么测试框架？" → 答 "Vitest"
   ⭐ 说明技能加载了
② grep -r "jest|vitest" .claude/skills/
   → 测试技能说 Vitest（对）
   → 一个旧的 code-review 技能说 "check Jest best practices"（错）
③ 读两个 description：
   code-review 的是 "Use this when reviewing code" —— 没有作用域
   ⭐ 所以在评审测试文件时被共同加载了
④ 删掉 code-review 里的 Jest 行，
   并把它的 description 收紧为
   "reviewing PRs against bug/security/performance criteria"
⑤ 重跑 → Vitest → 修好
```

> ⭐ **五分钟，因为顺序是对的：
> 确认加载 → 检查 description 作用域 → 找重叠。**

这正好对应 `troubleshooting-manual.md` 的四步法，
也验证了 `namespace-collision.md` 里
"两个技能都在场、互相稀释触发概率"的那个隐蔽表现。

---

## 速查

```
① 目录 + SKILL.md 全大写
② 位置对不对（个人 / 项目）
③ ⭐ 重启会话（或 /reload-plugins）
④ ⭐ description（头号原因）
⑤ frontmatter 合法（无 tab、有闭合 ---、无裸冒号）
⑥ 是否启用 / 是否设了 disable-model-invocation
⑦ 权限与 /tmp
⑧ ⭐ 显式调用做隔离
⑨ 客户端版本 + changelog

⭐ 隔离判据：显式能、自动不能 → 问题在 description
⭐ 误区：改文件必须重启（❌）、编号文件夹定优先级（❌）
```

**另一份五因速查**（不同来源，可交叉参考）：

| 原因 | 症状 | 修法 |
|---|---|---|
| 会话中途安装 | 技能完全不出现，连直接问都没有 | 新会话 / `/reload-plugins` |
| 路径错或双层嵌套 | 不在 `ls ~/.claude/skills/*/SKILL.md` 里 | 把 SKILL.md 上移一层 |
| frontmatter 坏 | 路径对但仍不列出 | 含冒号的描述加引号 |
| ⭐ 描述不匹配 | 手动调用能加载，但从不自动触发 | 用你真正会输入的触发词重写 |
| ⭐ 字符预算超了 | 多装了几个技能后，原本好用的不触发了 | 提高预算 / 精简描述 |
