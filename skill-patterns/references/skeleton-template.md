# 可直接抄的技能骨架（含六个必含小节）

> 相关：《skill-crafting》的 `creation-framework.md` ·
> 《skill-authoring》的 `template-skill.md` ·
> 《skill-patterns》的 `structure-modes-abcde.md`

---

## 目录

- [1. ⭐ 六个必含小节](#1--六个必含小节)
- [2. 完整骨架](#2-完整骨架)
- [3. ⭐ 触发调优：太频繁 vs 不触发](#3--触发调优太频繁-vs-不触发)
- [4. 指令 vs 脚本的选择](#4-指令-vs-脚本的选择)

---

## 1. ⭐ 六个必含小节

推荐正文包含这六个部分：

```
① When to use / When NOT to use   ⭐ 双向都要
② Required inputs                 必需输入
③ Step-by-step procedures         分步流程
④ Expected outputs                预期输出
⑤ Failure handling                失败处理
⑥ Definition of done              完成定义
```

> ⭐ 第 ① 条**双向都要写**——
> 只写"何时用"不写"何时不用"，技能会乱跑。
>
> ⭐ 第 ⑤ 条最常被漏，而它恰恰决定 agent 会不会卡死。

---

## 2. 完整骨架

```markdown
## Inputs Required
- Repository path
- Target branch
- Test command

## Procedure
1. Validate required inputs.
2. Analyze changed files and blast radius.
3. Run checks and capture failures.
4. Produce findings in severity order.

## Expected Outputs
- Markdown report at `reports/review.md`
- List of blocking issues
- Suggested remediation steps

## Definition of Done
- [ ] Inputs validated
- [ ] Changed files analyzed
- [ ] Report written
- [ ] ⭐ Blocking issues flagged
```

**让指令更可靠的四条**：

```
① ⭐ 用祈使步骤（"Do X, then Y"）
② 定义输出格式与成功标准
③ 点明边界情况与常见失败模式
④ 给出完成度定义
```

---

## 3. ⭐ 触发调优：太频繁 vs 不触发

**触发太频繁**时，可以调三处：

```
① 收窄 description
② ⭐ 加显式的 "do not use when" 边界
③ ⭐ 对有风险的工作流禁用隐式调用
```

**从不触发 / 触发不够**时：

```
① ⭐ 加具体的用户措辞与同义词
② ⭐ 加显式的 "use when..." 表述
③ ⭐ 确认目录名与 name 完全一致
```

> ⭐ 第 ③ 条很容易漏——
> **目录名与 frontmatter 的 name 必须一字不差**，否则找不到。

**触发的两种方式**：

```
隐式触发：把用户请求与 description 匹配
         User: "review this PR" → 匹配 review-pr 技能

显式触发：在工具 UI 里按名字调用
         User: /deploy
```

> ⭐ **显式应用于有风险的操作——
> 部署、迁移、任何破坏性动作。**
>
> ⭐ **可移植的最佳实践：总是先 plan，
> 只在显式确认后才 execute**，避免意外的副作用。

---

## 4. 指令 vs 脚本的选择

> ⭐ **判断法则：当正确性依赖计算、
> 或能用可复用片段校验时，就用脚本。**

| | 适用 |
|---|---|
| **纯指令技能** | ⭐ 策略或流程指导 —— 更可移植 |
| **脚本支撑技能** | ⭐ 转换、校验、报告生成、精确格式检查 |

> 与《skill-crafting》`scripts-as-production.md` 一致，
> 但这里给了更清晰的判据：**正确性是否依赖计算**。

**脚本五条最佳实践**：

```
① ⭐ 尽早校验依赖
② ⭐ 打印可操作的清晰错误
③ ⭐ 避免隐藏副作用
④ 非交互（TTY 会挂死）
⑤ 结构化输出（JSON/CSV，字段固定）
```

---

## 速查

```
□ 六小节：何时用/不用 · 必需输入 · 流程 · 预期输出 · 失败处理 · 完成定义
□ ⭐ "何时不用" 与 "何时用" 同等重要
□ ⭐ 失败处理决定 agent 会不会卡死
□ 祈使句 + 输出格式 + 边界情况 + 完成定义
□ ⭐ 触发太频繁 → 收窄 / 加 do not use when / 禁用隐式
□ ⭐ 不触发 → 加具体措辞 / 加 use when / 核对目录名
□ ⭐ 有风险操作用显式调用 + 先 plan 后 execute
□ ⭐ 正确性依赖计算 → 用脚本
□ 脚本：早校验依赖、清晰错误、无隐藏副作用
```

**规模约束**（再次确认）：

```
⭐ 正文 < 500 行 / 5,000 tokens
超出就拆：
  深层文档  → references/
  大示例    → references/examples.md
  模式与模板 → assets/
⭐ 全部用相对路径从 SKILL.md 链接
```

**一个技能 = 一个能力或工作流**：

> ⭐ 如果你发现自己想塞多个工作流进一个技能，
> **拆成多个技能，并在 description 里写清何时用哪个**。
