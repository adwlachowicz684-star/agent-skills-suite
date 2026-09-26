# 团队 SKILL.md 约定模板（含命名仲裁）

> 相关：《skill-gallery》的其余样本 ·
> 《skill-structuring》的 `naming-conventions.md` · `naming-gerund-form.md` ·
> 《skill-description》的 `description-four-rules.md` ·
> 《skill-crafting》的 `minimum-viable-three-principles.md`
> 前置：那些讲命名的各个侧面，
> 这份给一份⭐ 可直接落地的团队模板 +
> ⭐⭐⭐⭐ 一处⭐ 命名风格的⭐ 矛盾仲裁。

---

## 目录

- [1. ⭐⭐⭐ 模板](#1--模板)
- [2. ⭐⭐⭐⭐ 命名仲裁：verb-noun 还是动名词](#2--命名仲裁verb-noun-还是动名词)
- [3. ⭐⭐⭐ 五条约定](#3--五条约定)
- [4. ⭐⭐⭐ 尺寸目标表](#4--尺寸目标表)
- [5. ⭐⭐⭐ 两个常见问题的修法](#5--两个常见问题的修法)

---

## 1. ⭐⭐⭐ 模板

```yaml
---
name: [verb]-[noun]
description: >
  [What it does in one sentence]. Use when [trigger 1], [trigger 2], or [trigger 3].
argument-hint: "[expected-input]"
disable-model-invocation: false
allowed-tools: [space-separated tool list]
paths: "[glob pattern if scoped]"
---

# [Skill Name]

[One paragraph: what this skill does and when to use it. 2-3 sentences.]

## Steps
1. [First action, imperative form]
2. [Second action]
3. [Third action]

## Rules
- [Constraint 1: what to always do]
- [Constraint 2: what to never do]
- [Constraint 3: boundary condition]

## Output Format
[Exact format Claude should produce]

## References
For [detailed topic], read ${CLAUDE_SKILL_DIR}/references/[file].md
```

> ⭐⭐⭐ 几处值得学的设计：
> ```
> · ⭐⭐ `argument-hint` 把"预期输入是什么"暴露给⭐ 调用方（补全提示）
> · ⭐⭐⭐ `paths` 只在⭐ 需要限定时才写（模板里标注了 "if scoped"）
> · ⭐⭐⭐⭐ `## References` 用 ⭐ `${CLAUDE_SKILL_DIR}` ⭐ 而不是相对路径
>   （否则技能装到别处就失效——与 script-cli-contract.md 第 5 条一致）
> · ⭐⭐⭐ `## Rules` 三条 = ⭐ 永远做 / ⭐⭐⭐ 永远不做 / ⭐ 边界条件
>   ⭐⭐⭐ 这个三分法很实用：⭐ 多数技能只写了第一类
> ```

---

## 2. ⭐⭐⭐⭐ 命名仲裁：verb-noun 还是动名词

⭐⭐⭐⭐ **两份权威来源给出了不同建议**：

| 来源 | 建议 | 示例 |
|---|---|---|
| ⭐⭐⭐ Anthropic 官方 | ⭐ 动名词（verb + -ing） | `processing-pdfs` `analyzing-spreadsheets` `testing-code` |
| ⭐⭐⭐ 本团队规范 | ⭐ verb-noun | `generate-tests` `deploy-staging` `review-pr` `fix-lint` |

**官方的另外两种"可接受替代"**：

```
✅ 名词短语：pdf-processing, spreadsheet-analysis
✅ 动作导向：process-pdfs, analyze-spreadsheets
❌ 含糊：helper, utils, tools
❌ 过于通用：documents, data, files
❌ 保留字：anthropic-helper, claude-tools（⭐ name 不得含 anthropic/claude）
```

> ⭐⭐⭐⭐⭐ **仲裁：两者都对，⭐⭐⭐ 因为⭐⭐⭐ 官方明确把"动作导向"列为可接受替代。**
> ⭐⭐⭐⭐ 所以⭐ 真正的判据不是⭐ 动名词 vs verb-noun，
> ⭐⭐⭐⭐⭐ 而是⭐⭐⭐⭐ **一致性 > 形态**（这正是 `naming-conventions.md` 的结论）：
> ```
> ❌ 一个 writing-workflow-sops，下一个 sop-writer，第三个 create-sops
> ✅ ⭐⭐⭐⭐⭐ ⭐ 选定一个模式，⭐ 整套库都用它
> ```
>
> ⭐⭐⭐⭐ 一个⭐ 实操建议：
> ⭐⭐⭐⭐⭐ **动名词的优势在于⭐ 它天然读作"一种能力"而非"一个命令"**，
> ⭐⭐⭐ 这与"技能是⭐ 能力（capability）而非⭐ 命令"的定位一致；
> ⭐⭐⭐ 但⭐ verb-noun ⭐ 更短、⭐ 在命令行里打起来更快。
> ⭐⭐⭐ ⭐ **人少的团队选哪个都行，⭐⭐⭐⭐ 关键是⭐ 写进 CLAUDE.md 并⭐ 用 linter 强制。**

**用 CLAUDE.md 强制**（一个很实用的落地手法）：

```markdown
## Skills
Skill names follow verb-noun format with lowercase hyphens.
```

> ⭐⭐⭐ 这又是⭐ "书面规则编码成校验器"的实例——
> ⭐⭐⭐⭐ 但这里⭐ 更诚实：⭐ 写在 CLAUDE.md 里⭐ 只是让模型⭐ 更可能遵守，
> ⭐⭐⭐⭐ ⭐⭐ 真正强制要靠 ⭐ linter（`lint-tooling.md` 横评里有相关工具）。

---

## 3. ⭐⭐⭐ 五条约定

```
① ⭐⭐⭐ 命名：verb-noun · 小写 · 连字符
   ⭐⭐⭐ name 字段：仅小写字母、数字、连字符，⭐ 最长 64 字符
   ⭐⭐ 省略时⭐ 默认为目录名
   ⭐⭐⭐⭐ ⭐ 用具体名词：review-pr 而非 review，deploy-staging 而非 deploy

② ⭐⭐⭐⭐⭐ 描述：⭐⭐⭐⭐⭐ ⭐ 前置触发词
   ⭐⭐⭐⭐ "描述必须包含⭐ 用户自然会说的词。Claude 用这段文本做匹配。"
   ✅ "Generate unit tests for React components. Use when the user says
       'write tests', 'add test coverage', or 'test this component'."
   ❌ "Helps with testing stuff"
   ⭐⭐⭐⭐⭐ ⭐ description + when_to_use 合计上限 1,536 字符，会被截断
      → ⭐⭐⭐⭐ ⭐⭐ ⭐ 重要的触发词⭐ 放末尾可能被直接切掉 → ⭐ 主要用例前置

③ ⭐⭐⭐ 正文：⭐ 祈使句，⭐ 不用第二人称
   ✅ "Run the test suite."  ❌ "You should run the test suite."

④ ⭐⭐⭐⭐⭐ 有副作用的技能：⭐⭐⭐⭐⭐ 必须手动调用
   ⭐⭐⭐⭐⭐ ⭐ 创建文件、提交代码、部署、发邮件、改外部状态
      → ⭐⭐⭐⭐⭐ ⭐ `disable-model-invocation: true`
   ⭐⭐⭐⭐⭐ ⭐ 否则 Claude 可能⭐ 在它认为相关时⭐ 自动触发，造成⭐ 非预期副作用
   deploy / commit / send-email / create-ticket / run-migration / delete-branch

⑤ ⭐⭐⭐ 尺寸：见第 4 节
```

> ⭐⭐⭐⭐ 第 ④ 条是⭐ "确定性判断要用确定性机制承载"的
> ⭐⭐⭐⭐⭐ **第六个独立来源**，而且⭐⭐ 官方措辞最强：
> ⭐⭐⭐⭐⭐ **"MUST have disable-model-invocation: true"**。
> ⭐⭐⭐⭐ 与我们已有的 `allowed-tools-reference.md`、
> `seven-contracts.md`（"不能被'完成任务'这个宽泛目标自动授权"）
> ⭐⭐⭐ 完全同源。

---

## 4. ⭐⭐⭐ 尺寸目标表

| 内容位置 | ⭐ 目标 |
|---|---|
| ⭐⭐⭐ 触发元数据（frontmatter） | ⭐ < 1,536 字符 |
| ⭐⭐⭐ 核心指令（SKILL.md 正文） | ⭐⭐ 1,500–2,000 词 |
| ⭐⭐ 详细参考（references/*.md） | ⭐ 每份 2,000–5,000 词 |
| 模板（templates/*.md） | 按需 |
| 脚本（scripts/*） | 按需 |

> ⭐⭐⭐⭐ 硬约束一句：
> ⭐⭐⭐⭐ **"⭐ 永远不要把一份 5,000 词的参考文档放进 SKILL.md 正文。
> ⭐⭐⭐⭐ 移到 references/ 并加一行：
> ⭐ 'For detailed X, read ${CLAUDE_SKILL_DIR}/references/x.md。'"**

> ⭐⭐⭐⭐ 这张表⭐ 补上了一个我们此前⭐ 有争议的尺寸口径：
> 我们记过 30–60（理想）/ 150–300（健康）/ 500 行（硬上限），
> ⭐⭐⭐ 而这里给的是⭐ 词数：1,500–2,000 词。
> ⭐⭐⭐⭐ 两者⭐ 大致自洽（⭐ 中英差异会拉开）：
> ⭐⭐ 英文 1,500 词 ≈ 150–200 行；⭐⭐ 中文 1,500–2,000 "词"会更短。
> ⭐⭐⭐⭐⭐ ⭐ 实操建议：⭐⭐⭐⭐ **以⭐ 行数为硬门禁（<500 行），
> ⭐⭐⭐ 以⭐ "能不能一眼看完"为软目标**——
> ⭐⭐⭐⭐ 因为⭐ 词数在不同语言下不具可比性。

---

## 5. ⭐⭐⭐ 两个常见问题的修法

```
① ⭐⭐⭐ 命名在技能间不一致
   → ⭐⭐⭐⭐ ⭐ 在 CLAUDE.md 里加一条规则强制（见第 2 节末尾）

② ⭐⭐⭐⭐ ⭐ 两个技能的描述太像，⭐ 抢同一个触发
   ⭐⭐⭐⭐⭐ "两个描述里都含 'review code' 的技能会⭐ 互相竞争"
   → ⭐⭐⭐⭐⭐ ⭐ 差异化：一个说 "review pull request changes"，
                  另一个说 "review code style and formatting"
```

> ⭐⭐⭐⭐⭐ 第 ② 条⭐ 给出的修法很具体，值得单独抄：
> ⭐⭐⭐⭐ **不要只加否定词，要⭐ 各自⭐ 换用⭐ 不同的动词/宾语搭配**
> （"review PR 的改动" vs "review 代码风格与格式"）。
> ⭐⭐⭐ 这与 `description-scope-shape.md` 的"排除声明互相点名"、
> `trigger-tuning-loop.md` 的"误触发加反触发"
> ⭐⭐ 一致，但⭐⭐⭐⭐ 这里更进一步：⭐ **从源头避免重叠，而不是事后打补丁。**
>
> ⭐⭐⭐⭐ 另一个相关信号（来自官方）：
> ⭐⭐⭐ **如果两个技能 80% 相同，⭐⭐⭐⭐ 考虑合并成一个、内部按条件分支**
> （与 `trigger-tuning-loop.md`/`nine-anti-patterns.md` 的结论一致）。

---

## 速查

```
□ ⭐⭐⭐ 模板要点：argument-hint 暴露预期输入 · paths 只在需要时写
   ⭐⭐⭐⭐ References 用 ⭐ ${CLAUDE_SKILL_DIR} ⭐（不用相对路径）
   ⭐⭐⭐ Rules 三条 = 永远做 / ⭐⭐⭐ 永远不做 / ⭐ 边界条件（多数技能只写了第一类）
□ ⭐⭐⭐⭐⭐ 命名仲裁：官方推⭐ 动名词，团队规范推⭐ verb-noun
   ⭐⭐⭐⭐⭐ ⭐ 官方把"动作导向"列为可接受替代 → ⭐⭐⭐⭐ ⭐ 一致性 > 形态
   ⭐⭐⭐⭐ 动名词读作"能力"、verb-noun 更短好打 → 选一个、写进 CLAUDE.md、用 linter 强制
□ ⭐⭐⭐⭐⭐ 描述⭐⭐⭐⭐⭐ 前置触发词；合计上限 1,536 字符会截断 → ⭐ 主要用例前置
□ ⭐⭐⭐⭐⭐ 有副作用 → ⭐⭐⭐⭐⭐ MUST disable-model-invocation: true
   deploy / commit / send-email / create-ticket / run-migration / delete-branch
□ ⭐⭐⭐⭐ 尺寸：frontmatter<1,536字符 · 正文 1,500–2,000词 · 每份 reference 2,000–5,000词
   ⭐⭐⭐⭐ ⭐ 以行数为硬门禁(<500)，以"能不能一眼看完"为软目标（词数跨语言不可比）
   ⭐⭐⭐⭐ ⭐ 绝不要把 5,000 词的文档放正文
□ ⭐⭐⭐⭐⭐ 描述太像抢触发 → ⭐⭐⭐⭐ ⭐ 换不同的动词/宾语搭配（从源头避免重叠）
   ⭐⭐⭐ 80% 相同 → 合并成一个内部分支
```

**一句话**：

> ⭐⭐⭐⭐ **官方推动名词、团队规范推 verb-noun 看似矛盾，但官方明确把"动作导向"列为可接受替代，所以真正的判据是一致性 > 形态——选一个、写进 CLAUDE.md、用 linter 强制；而最有约束力的一条是有副作用的技能 MUST 设 `disable-model-invocation: true`。**
