# 元技能：让 agent 自己写技能

> 相关：《skill-authoring》的 `reproduction.md` ·
> 《skill-orchestration》的 `subagents.md` ·
> 《skill-crafting》的 `skill-structuring` 的 `frontmatter-fields.md`

---

## 目录

- [1. 四种技能来源](#1-四种技能来源)
- [2. ⭐ 模式四：元技能（技能工厂）](#2--模式四元技能技能工厂)
- [3. ⭐ 关键设计：references 里放规范与范例](#3--关键设计references-里放规范与范例)
- [4. 六条生成规则](#4-六条生成规则)
- [5. ⭐ 必须保留人在环路](#5--必须保留人在环路)

---

## 1. 四种技能来源

| 模式 | 来源 | 说明 |
|---|---|---|
| ① Inline | 直接写在代码里 | 简单清单 |
| ② ⭐ File-based | 自己写的目录 | `load_skill_from_dir()` |
| ③ External | 从社区下载 | ⭐ **代码与模式二完全相同** |
| ④ ⭐ Meta | agent 自己生成 | 见下 |

> ⭐ 模式二与模式三的**调用代码完全一样**——
> 因为规范定义了通用目录格式，加载器不关心 SKILL.md 是写的还是下载的。
> 这正是"技能是纯 Markdown、协议无关"的价值。

---

## 2. ⭐ 模式四：元技能（技能工厂）

> ⭐ **元技能 = 目的就是生成新 SKILL.md 的技能。
> 装备了它的 agent 变成"自扩展"的——
> 可以在运行时编写并加载新的技能定义，无需人工干预。**

```
skill-creator:
  name: "Creates new ADK-compatible skill definitions from requirements."
  description: "Generates complete SKILL.md files following the
                Agent Skills specification at agentskills.io."
```

---

## 3. ⭐ 关键设计：references 里放规范与范例

```
resources.references = {
  "skill-spec.md":    "# Agent Skills Specification (agentskills.io)...",
  "example-skill.md": "# Example: Code Review Skill...",
}
```

指令：

```
When asked to create a new skill, generate a complete SKILL.md file.
Read `references/skill-spec.md` for the format specification.
Read `references/example-skill.md` for a working example.
```

> ⭐ **这是元技能能否工作的关键**：
> 不是让模型凭记忆写 SKILL.md，
> 而是**把规范本身和一份可运行范例作为 L3 资源嵌入**。
>
> 模型在生成前读这两份，产出才合规。

这套设计完全可以迁移——
**我们的 `skill-authoring` 就是这个思路**：
把规范和范例放在 references 里，让模型照着生成。

---

## 4. 六条生成规则

```
1. name 必须 kebab-case，最多 64 字符
2. ⭐ description 必须少于 1024 字符
3. 指令清晰、分步骤
4. 详细领域知识放 references/
5. ⭐ SKILL.md 保持在 500 行以内，细节放 references/
6. ⭐ 输出完整文件内容，让用户可以直接保存
```

> 第 6 条容易被漏——
> **让模型输出完整文件而不是"你可以这样写"**，
> 用户才能直接落地。

---

## 5. ⭐ 必须保留人在环路

> ⭐ **虽然自动生成技能很强大，建议保留人工复核最终 SKILL.md。**
>
> **并且，对你构建的任何技能，都应该测试其有效性。**

理由与 `code-review-trust.md` 那条一致：

> ⭐ **别让 AI 给自己的作业打分。**
> 生成的技能必须通过独立测试才算数。

**工厂运作示例**：

```
用户："我需要一个新技能，用来审查 Python 代码的安全漏洞。"

agent 加载 skill-creator
  → 读 skill-spec.md（规范）
  → 读 example-skill.md（范例）
  → 生成完整的 Python 安全审查技能
     合规命名、结构化指令（输入校验、认证、密码学）、
     按严重度的报告格式
  → ⭐ 人工复核
  → ⭐ 跑评估
```

生成的技能遵循同一规范，
所以**不只在一个平台能用**——
任何兼容格式的产品都能加载。

---

## 速查

```
□ 元技能的 references 里必须有：规范 + 可运行范例
□ 生成规则写清（命名、长度、500 行、放 references）
□ ⭐ 输出完整文件内容，可直接保存
□ ⭐ 生成后必须人工复核
□ ⭐ 生成后必须跑评估（不能凭"看起来对"）
□ 依赖规范通用性，才能跨平台
```

**一个提醒**：

> ⭐ 自扩展能力很强大，但也意味着
> **技能库会以你无法预见的速度增长**。
> 配套必须要有 `library-ops.md` 里那套清理机制，
> 否则很快就会撞上 `library-size-effect.md` 说的遮蔽问题。
