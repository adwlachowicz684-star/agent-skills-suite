# 九个技能反模式（含症状、根因、修法）

> 相关：《skill-refining》的 `pruning.md` · `skill-structuring` 的 `what-not-to-ship.md` ·
> 《skill-crafting》的 `anti-pattern-section.md`

---

## 目录

- [1. 八股文式步骤](#1-八股文式步骤)
- [2. 内容倾倒](#2-内容倾倒)
- [3. 孤儿引用](#3-孤儿引用)
- [4. 打勾式流程](#4-打勾式流程)
- [5. ⭐ 模糊警告](#5--模糊警告)
- [6. 隐身技能](#6-隐身技能)
- [7. ⭐ 位置错误](#7--位置错误)
- [8. 过度工程](#8-过度工程)
- [9. ⭐ 自由度错配](#9--自由度错配)

---

## 1. 八股文式步骤

| | |
|---|---|
| **症状** | 机械的 Step 1、Step 2、Step 3 |
| **根因** | ⭐ 作者按**流程**思考，而不是按**思维框架** |
| **修法** | 转成 "Before doing X, ask yourself..."；⭐ 聚焦决策原则而非操作序列 |

---

## 2. 内容倾倒（The Dump）

| | |
|---|---|
| **症状** | SKILL.md 800+ 行，什么都塞进去 |
| **根因** | 没有渐进式披露设计 |
| **修法** | ⭐ 核心路由与决策树留在 SKILL.md（理想 <300 行）；详细内容进 `references/` |

---

## 3. 孤儿引用（The Orphan References）

| | |
|---|---|
| **症状** | `references/` 存在，但文件从没被加载过 |
| **根因** | 没有明确的加载触发 |
| **修法** | ⭐ 在工作流的决策点写 "MANDATORY - READ ENTIRE FILE"<br>⭐ 并写 "Do NOT Load" 防止过度加载 |

> ⭐ 双向都要写——**只说"要读"不说"别读"，模型会全读一遍。**

---

## 4. 打勾式流程（The Checkbox Procedure）

见第 1 条，两者同源。补充一点：

> ⭐ 例外：**Pipeline 模式确实需要显式步骤**——
> 因为它的核心约束维度就是执行顺序。
> 所以这条反模式针对的是**本该给原则却给了流程**的情况。

---

## 5. ⭐ 模糊警告（The Vague Warning）

| | |
|---|---|
| **症状** | "小心一点"、"避免错误"、"考虑边界情况" |
| **根因** | 作者知道会出问题，但没说清具体是什么 |
| **修法** | ⭐ 具体的 NEVER 清单，⭐ 带具体例子和**非显而易见的理由** |

```
⭐ 模板："NEVER use X because [需要经验才知道的具体问题]"
```

> 这条与 `pruning.md` 的 no-op 测试直接对应：
> **"要小心" 删掉后模型行为不变 = 空操作句**；
> 而 "NEVER X because Y" 删掉会改变行为。

---

## 6. 隐身技能（The Invisible Skill）

| | |
|---|---|
| **症状** | 内容很好，但几乎从不被激活 |
| **根因** | description 含糊、缺关键词、缺触发场景 |
| **修法** | ⭐ description 必须回答 WHAT、WHEN，并含 KEYWORDS |

```
❌ "Helps with document tasks"
✅ "Create, edit, and analyze .docx files. Use when working with
   Word documents, tracked changes, or professional document formatting."
```

---

## 7. ⭐ 位置错误（The Wrong Location）

| | |
|---|---|
| **症状** | "When to use this Skill" 写在正文里，不在 description 里 |
| **根因** | ⭐ 误解了三层加载机制 |
| **修法** | ⭐ 所有触发信息移到 description 字段<br>⭐ **正文是在触发决策做出之后才加载的** |

> ⭐ 这是最根本的一个：
> **写在正文里的触发条件，模型在决定是否触发时根本看不到。**
> 与 `skill-structuring` 的 `frontmatter-pitfalls.md` 的两阶段解析是同一件事的两个面。

---

## 8. 过度工程（The Over-Engineered）

| | |
|---|---|
| **症状** | README.md、CHANGELOG.md、INSTALLATION_GUIDE.md、CONTRIBUTING.md |
| **根因** | ⭐ 把技能当成软件项目 |
| **修法** | 删掉所有辅助文件——只保留 agent 完成任务所需的东西<br>⭐ **不要有关于技能本身的文档** |

---

## 9. ⭐ 自由度错配（The Freedom Mismatch）

| | |
|---|---|
| **症状** | 创意任务给死板脚本；脆弱操作给含糊指引 |
| **根因** | ⭐ 没考虑任务脆弱性 |
| **修法** | 创意 → 高自由度（给原则）；脆弱 → 低自由度（给精确脚本、无参数） |

> 与 `skill-principles.md` 的自由度校准完全一致——
> **两侧悬崖的窄桥给护栏，开阔地给方向。**

---

## 速查表

```
□ 有 Step1/2/3 但本该给原则     → 改 "Before doing X, ask yourself"
□ 主文件 >300 行                → 拆进 references
□ references 从没被加载          → 加 MANDATORY + Do NOT Load
□ "要小心/避免错误"              → 换成 NEVER X because Y
□ 技能从不触发                   → description 补 WHAT/WHEN/关键词
□ ⭐ 触发条件写在正文             → ⭐ 移到 description（正文触发后才加载）
□ 有 README/CHANGELOG           → 删掉
□ ⭐ 创意任务给死脚本            → 给原则
□ ⭐ 脆弱操作给含糊指引          → 给精确脚本、无参数
```

**元问题**（评估任何技能时回到这一句）：

> ⭐ **"这个领域的专家看到这个技能，会说：
> '是的，它抓住了我花好几年才学会的东西' 吗？"**
