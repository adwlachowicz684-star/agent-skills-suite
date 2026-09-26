# 操作卡写法：Keep / Delete 清单与 30–60 行目标

> 相关：《skill-authoring》的 `skill-anatomy.md` ·
> 《skill-gallery》的 `first-skill-minimal.md` ·
> `token-bloat-audit.md`
> 前置：那些讲"结构是什么"，
> 这份给⭐ **一份可照抄的取舍清单**：正文里该留什么、该删什么、目标多长。

---

## 目录

- [1. ⭐⭐ SKILL.md 是一张操作卡](#1--skillmd-是一张操作卡)
- [2. ⭐⭐⭐ Keep / Delete 清单](#2--keep--delete-清单)
- [3. ⭐ 30–60 行目标与 120 行上限](#3--3060-行目标与-120-行上限)
- [4. ⭐⭐ description 公式](#4--description-公式)
- [5. ⭐ 正向指针会悬空，负向指针不会](#5--正向指针会悬空负向指针不会)

---

## 1. ⭐⭐ SKILL.md 是一张操作卡

> ⭐ **把 SKILL.md 草稿写成一张"操作卡"（operator card），
> 而不是一篇说明文。**

操作卡只回答四个问题：

```
① ⭐ 跑什么        what to run
② ⭐ 什么时候跑    when to run it
③ ⭐ 输出意味着什么 what output means
④ ⭐ 哪些坑要紧    what traps matter
```

> ⭐⭐ 第 ③ 条"输出意味着什么"是多数技能漏掉的一项——
> 它给出步骤、给输出格式，但**不说"看到这个输出说明什么、下一步怎么办"**。
> 这正是 `script-cli-contract.md` 说"模型靠退出码判断"的那个道理的正文版。

**澄清只问缺的**（避免反复打断）：

```
只澄清缺失的必需项：
   能力 · 触发条件 · 反触发条件 · 工具/脚本需求 · 可移植性
⭐ 其他一律不问
```

---

## 2. ⭐⭐⭐ Keep / Delete 清单

**保留**：

```
✅ ⭐ 可运行的命令，或确切的工作流步骤
✅ ⭐ 常见会卡住首次使用的"就绪检查"（setup checks）
✅ 精简的输出契约
✅ ⭐ 路由边界与安全陷阱
✅ ⭐ 每个命令或概念配一个⭐ 强示例
```

**删除**（这一段最有价值，因为每一条都是我们默认会写的）：

```
❌ ⭐ 复述 description 的概述性散文
❌ ⭐ 安装 / 贡献 / 隐私 / 排障章节
   ——⭐ 除非它们会改变 agent 的行为
❌ ⭐ 复制过来的 CLI help、schema、flag 目录、生成文档
❌ 重复的提示词示例与套话分析
❌ ⭐ README、references、helper 脚本里已经有的细节
```

> ⭐⭐⭐ **"除非它会改变 agent 行为"** 是这整段的裁决标准：
> 安装说明、贡献指南、隐私声明——**都是给人看的，agent 读了行为不变，
> 就是纯 token 浪费**。

> ⭐ "复制过来的 CLI help / flag 目录"这条很实用：
> 正确做法是**写 `Run <tool> --help` 看全部 flag，技能里只留非显然的 flag**
> ——又是一个"能查就别抄"的例子（呼应确定性优先）。

**工具型技能的特殊写法**：

```
⭐ 把确定性工作放进 scripts/ 或已有的可执行文件
⭐ SKILL.md 退化成⭐ "调用菜单 + 输出形状 + 坑"
```

---

## 3. ⭐ 30–60 行目标与 120 行上限

```
工具包装型（tool wrapper）  ⭐ 30–60 行
一般上限                    ⭐ ~120 行
```

> ⭐ 这里出现了一个比主套件常用的 500 行更严的口径。
> 两者不矛盾：**500 行是硬边界（物理截断），120 行是质量目标**。
> 这与 `budget-truncation.md` 的"压缩后只留前 5,000 tokens"一致——
> **越短，被完整保留的概率越高。**

**如果 setup 很长**：

```
✅ 就绪检查内联在 SKILL.md
✅ ⭐ 完整操作指南移到"一跳之外"（references/）
```

---

## 4. ⭐⭐ description 公式

```
description: Use when [触发条件] — [具体能力]. Handles [文件类型/上下文/症状/同义词].

✅ 好：
   Use when working with PDF files — extracts text, fills forms,
   merges documents. Handles .pdf files, scanned PDFs, and form fields.

❌ 坏：
   Processes PDFs by first extracting text, then analyzing structure,
   then outputting results.
```

> ⭐⭐ 坏例子的问题正是 `skill-anatomy-antipatterns.md` 那条
> **"绝不在 description 里总结工作流——Claude 可能照着它抄近路"**。
> 两个独立来源给出了同一个禁令。

**要包含**：

```
✅ ⭐ 用户真正会说的词
✅ ⭐ 文件类型与扩展名
✅ ⭐ 错误信息或症状
✅ 同义词与替代表述
✅ ⭐ 当误报代价高时，写明正向/负向触发的区分
```

**要排除**：

```
❌ 逐步的工作流摘要
❌ 实现细节
❌ ⭐ 第一人称
❌ "helps with documents" 这类笼统声称
```

**其他硬性规则**（与主套件已有条目一致，这里汇总）：

```
· 1–3 句，⭐ 第三人称，现在时
· 第 1 句点明具体能力
· ⭐ 第 2 句以 "Use when ..." 开头，列出真实触发词
· 对宽泛领域加 "Do NOT use ..."（review / search / docs / git / browser）
· 避免营销词、时效性声称、以及重复的"this skill should be used when"
```

> ⭐ "第三人称"的理由给得很实在：**它是作为元数据被注入的，
> 不是 agent 说出的话**。这与 `imperative-style.md` 讲的"you 指代不确定"
> 是同一件事的另一面。

---

## 5. ⭐ 正向指针会悬空，负向指针不会

一个很细腻但很实用的发现：

```
负向指针：Do NOT use for charts（用 dataviz）
   → ⭐ 即使 dataviz 不存在，也⭐ 无害降级（只是少了个提示）

正向指针：run X first
   → ⭐ X 不存在就会⭐ 悬空（dangle）
   → ⭐ 所以正向指针⭐ 必须指向一个确实存在的技能
```

> ⭐⭐ 这条解释了为什么"NOT for X → 用 Y 代替"这个句式这么强：
> **它同时是路由提示和边界声明，而且失败了也不会造成伤害。**
> 这正是 `description-scope-shape.md` 与 `namespace-collision.md`
> 都推荐的写法——现在有了机制上的解释。

**跨技能指针的另一条纪律**：

```
⭐ 指向的技能必须真的存在于 skills/ 里
```

---

## 速查

```
□ ⭐⭐ SKILL.md = 操作卡：跑什么·何时跑·⭐ 输出意味着什么·哪些坑
□ 澄清只问缺失项（能力/触发/反触发/工具/可移植性）

⭐⭐⭐ Keep：
□ 可运行命令或确切步骤 · ⭐ 首次使用的就绪检查
□ 精简输出契约 · ⭐ 路由边界与安全陷阱 · ⭐ 每个概念一个强示例

⭐⭐⭐ Delete：
□ ⭐ 复述 description 的概述散文
□ ⭐ 安装/贡献/隐私/排障章节（⭐ 除非会改变 agent 行为）
□ ⭐ 复制的 CLI help、schema、flag 目录
□ 重复示例 · ⭐ 别处已有的细节

□ ⭐ 30–60 行（工具型）· ~120 行上限 · 500 行是物理边界
□ setup 长 → 就绪检查内联，指南移一跳之外
□ 工具型：脚本承担确定性工作，SKILL.md = 调用菜单+输出形状+坑

⭐⭐ description 公式：
□ Use when [触发] — [能力]. Handles [类型/症状/同义词].
□ 含：⭐ 用户真说的词 · ⭐ 文件扩展名 · ⭐ 错误信息 · 同义词
□ 除：工作流摘要 · 实现细节 · ⭐ 第一人称 · 笼统声称
□ 1–3 句 · ⭐ 第三人称（它是被注入的元数据，不是 agent 说的话）

□ ⭐⭐ 负向指针无害降级，正向指针会悬空 → ⭐ 正向必须指向存在的技能
```

**一句话**：

> ⭐⭐ **安装、贡献、隐私、排障这些章节——除非它们会改变 agent 的行为，
> 否则一律删掉：agent 读了行为不变，就是纯 token 浪费。**
