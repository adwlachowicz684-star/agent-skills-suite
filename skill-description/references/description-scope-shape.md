# description 的句式、反触发与"一技能一动词"

> 相关：《skill-crafting》的 `description-by-collision-risk.md`（在 evaluating）·
> 《skill-evaluating》的 `description-by-collision-risk.md`
> 前置：那份讲"按碰撞风险决定长度"，
> 这份讲⭐ **句式模板、反触发的质量判据、以及范围蔓延**。

---

## 目录

- [1. ⭐ 前置条件句式](#1--前置条件句式)
- [2. ⭐⭐ 反触发：写不出三条就别发布](#2--反触发写不出三条就别发布)
- [3. ⭐ 一技能一动词一范围](#3--一技能一动词一范围)
- [4. 反例：三类不合格的 description](#4-反例三类不合格的-description)
- [5. ⭐ 太宽与太窄的两种死法](#5--太宽与太窄的两种死法)

---

## 1. ⭐ 前置条件句式

> ⭐ **把你的 description 用这个形式读回来：**
>
> ```
> When [触发条件], [动作动词] [范围] [可选的关注点].
> Skip if [否定条件].
> ```
>
> ⭐ **如果塞不进这个句式，那它多半太含糊了。**

**三个通过测试的样例**（值得抄的是它们都包含了 Skip）：

```
"When the user asks to deploy a Lambda function or mentions sam deploy,
 package and deploy via the AWS SAM CLI using the project's samconfig.toml.
 ⭐ Skip if the deployment is to production without an explicit
   confirmation flag."

"When the user pastes a stack trace or asks to debug a Python error,
 parse the traceback, identify the failing module and line,
 suggest 2-3 likely root causes ranked by probability.
 ⭐ Skip if the user already has a clear hypothesis."

"When the user asks to write a commit message or wants help summarizing
 a diff for git, generate a Conventional Commits-formatted message.
 ⭐ Skip if the user has already drafted a message and is asking for review."
```

> ⭐ 第三条尤其妙：**"用户已经写好草稿只是请你看"也要排除**——
> 这正是最常见的误触发场景。

**长度建议**：⭐ 控制在约 500 字符内（过长会在部分 UI 被截断，也会挤占发现上下文）。

---

## 2. ⭐⭐ 反触发：写不出三条就别发布

> ⭐⭐ **如果我写不出三条具体的反触发条件，
> 说明我对这个技能的范围理解得还不够，还不能发布。**
>
> ⭐ **列出"它不该做什么"这个练习，
> 正是你发现"它该做什么"的方式。**

**两条理由**（第二条是我认为最容易被忽略的）：

```
① ⭐ 十技能加载、三个都可能匹配时，
   ⭐ 否定范围写得最干净的那个，
   ⭐ 更容易赢下该赢的匹配、输掉不该赢的匹配

② ⭐⭐ 即使技能确实被调用了，显式的"超出范围"清单
   ⭐ 能防止它在任务中途扩大范围（scope creep）
```

**第 ② 条的对照极其具体**：

```
没有它：代码评审技能被叫去评审一个 typo 修复
       → ⭐ 会"好心"加上五段无关的架构反馈
有它：  "这是 typo 修复，不需要评审" → 停
```

**反触发的质量判据**：

```
❌ 坏的反触发："不要用于无关任务"
   ⭐ 这是同义反复（tautology），Claude 会当噪音处理

✅ 好的反触发：⭐ 点名具体的请求形态、具体的文件类型、具体的用户意图
   ⭐ 越具体越好
```

---

## 3. ⭐ 一技能一动词一范围

> **范围蔓延是仅次于"反触发太弱"的第二大错误。**

```
"我做一个 git-helper 技能"听起来合理
六周后它覆盖了：提交信息、分支命名、合并冲突、rebase、
                PR 描述、GitHub release、tag 管理

⭐ description 必须覆盖全部 → ⭐ 结果哪一个都没覆盖好
   → Claude 的匹配变得不可靠
```

**判据**（简单到可以立刻用）：

> ⭐⭐ **如果你在 description 里写"或"超过一次，那它多半是两个技能。**

**一个臃肿 git-helper 的拆法**（可直接照抄这个拆法）：

| 技能 slug | 触发词 | 范围 |
|---|---|---|
| git-commit-message | "write a commit message" | 从 staged diff 生成 Conventional Commits |
| git-branch-name | "name this branch" | 从 issue 生成 kebab-case 分支名 |
| git-rebase-help | "rebase" / "squash" | 走一遍交互式 rebase 决策 |
| git-pr-description | "write a PR" | 从提交日志生成 PR 标题与正文 |

> ⭐ **四个小技能胜过一个大技能**，三个理由（第一条最关键）：
> **匹配更锋利**。

---

## 4. 反例：三类不合格的 description

**① 太泛**

```
❌ "A skill for code review."
   没有触发短语、没有范围、没有反触发
   ⭐⭐ 两种失败模式都走一遍：
       要么每次提到 code 都触发（假阳性）
       要么模型学到"这是个噪音匹配"然后开始忽略它（假阴性）
```

> ⭐ "要么全触发要么永不触发，两种都毁掉体验"——
> 这个说法比"要写得具体"有效得多，因为它说清了**后果**。

**② ⭐ 是一份迷你手册**

```
❌ "先收集需求，然后搜索，然后写大纲，然后起草报告，
    然后根据反馈修改，并且总是使用清晰语言和带引用的要点..."
```

> ⭐⭐ 问题：**流程细节属于正文，写着这里有两个害处**
> ```
> ① 太长，在目录扫描时有截断风险
> ② ⭐ 运行时只读 description 做匹配——流程细节对激活毫无帮助
> ```
> 这与 `skill-anatomy-antipatterns.md` 的"绝不在 description 总结工作流"
> 完全一致（模型会照着 description 抄近路）。

**③ 缺"何时不用"**

```
❌ "This skill reviews code changes and suggests improvements."
   ⭐ 会对每一个编码请求都激活：写新功能、调试、重构、评审 PR
```

✅ 好的版本要点名四要素：**具体输入**（diffs/PRs）、**具体技术栈**（TS/React）、**关注维度**（正确性/可读性/性能/测试）、**清晰边界**（评审 vs 实现）。

---

## 5. ⭐ 太宽与太窄的两种死法

```
太窄的例子：
  "Check if Java HashMap usage follows thread-safety best practices."
  ⭐ 用户只想做一般性代码审查时，这条就匹配不上

太宽的例子：
  "A useful skill for developers."   ← 等于什么都没说
```

**平衡的做法**：

```
✅ "Review code changes for bugs, security vulnerabilities,
    performance issues, and style violations.
    Use when the user asks to check, review, or audit code quality
    in any programming language."
   ① 明确列出能力范围（bugs/security/performance/style）
   ② 指出触发关键词（check/review/audit）
   ③ ⭐ 不限定具体语言，保持合理的覆盖面
```

> ⭐ 第三条是个重要提醒：**精确 ≠ 越窄越好**。
> 关键是**"能力边界"和"触发条件"都要有**，而不是一味收窄。

**语言选择**：⭐ 建议统一用英文（官方规范与示例全英文、token 效率通常更优、团队协作通用性更好）。

---

## 速查

```
⭐ 句式：When [触发], [动词] [范围] [关注点]. Skip if [否定].
□ ⭐ 塞不进这个句式 = 太含糊
□ ⭐ 长度控制在约 500 字符内

⭐⭐ 反触发：
□ ⭐⭐ 写不出三条具体反触发 → 说明还没理解范围，别发布
□ ⭐⭐ 作用②：防止任务中途 scope creep
      （评审 typo 修复时不会加五段无关架构反馈）
□ ❌ "不要用于无关任务" = 同义反复，模型当噪音
□ ✅ 点名具体请求形态 / 文件类型 / 用户意图

⭐ 范围：
□ ⭐⭐ description 里"或"出现超过一次 = 多半该拆成两个
□ 一技能一动词一范围
□ 四小 > 一大（匹配更锋利）

❌ 三类不合格：
□ 太泛（要么全触发要么永不触发，两种都毁体验）
□ ⭐ 迷你手册（流程属于正文；且有截断风险 + 对激活无帮助）
□ 缺"何时不用"

□ ⭐ 精确 ≠ 越窄；能力边界与触发条件都要有
□ 建议英文
```

**一句话**：

> ⭐⭐ **写不出三条具体的反触发，说明你对范围的理解还不够——
> 而"列出它不该做什么"这个练习，正是你发现"它该做什么"的方式。**
